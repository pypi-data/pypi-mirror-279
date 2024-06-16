import os
import re
import shutil

import requests
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .AWSStorage import AwsS3Storage
from .StorageConstants import LOGGER_CODE_OBJECT, AWS_DEFAULT_STORAGE_BUCKET_NAME, AWS_DEFAULT_REGION


class Storage(GenericCRUD, metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name='storage', default_table_name='storage_table',
                         default_view_table_name='storage_view', default_column_name='storage_id')
        # TODO: get_s3 per region & bucket, according to user location.
        # TODO aws_bucket_name=get_aws_bucket_name( user_context )
        # TODO aws_region = get_aws_region( user_context )
        self.s3 = AwsS3Storage(bucket_name=AWS_DEFAULT_STORAGE_BUCKET_NAME, region=AWS_DEFAULT_REGION)
        self.is_test_data = is_test_data

    # returns the folder name from DB according to file_type_id
    def _get_file_type_by_file_type_id(self, file_type_id: int) -> str:
        file_type = self.select_one_value_by_column_and_value(view_table_name="file_type_view",
                                                              column_name="file_type_id",
                                                              column_value=file_type_id,
                                                              select_clause_value="file_type")
        return file_type

    def _get_region_and_folder_by_file_type_id(self, file_type_id: int) -> [str, str]:
        folder = self._get_file_type_by_file_type_id(file_type_id)
        # TODO Replace with a new method in user-context: region = user-context.get_effective_region()
        return [folder, AWS_DEFAULT_REGION]

    #
    def put(self, file_type_id: int, local_file_path: str) -> int:
        """uploads a file from the local computer to S3 and returns the storage_id of the file in the storage DB

        Args:
            profile_id int: user ID
            file_type_id int: type of the file - 
                                1 - Profile Image
                                2 - Coverage Image
                                3 - Personal Introduction Video
                                4 - Scanned Diving License 
                                5 - Scanned Passport
            filename string: file name including extension, i.e.test.txt
            local_file_path string: path to the file location, i.e. path/to/file/
        Returns:
            int: ID of the file in the storage DB
        """
        folder_and_region = self._get_region_and_folder_by_file_type_id(file_type_id)
        storage_id = self.s3.upload_file(local_file_path=local_file_path,
                                         remote_path=folder_and_region[0] + '/')
        return storage_id

    @staticmethod
    def preserve_letters_from_string(input_string: str) -> str:
        """Preserves only letters and spaces in a given string

        Args:
            input_string string: unmodified string
        """
        # Use a regular expression to match only letters (A-Z and a-z)
        pattern = r"[^a-zA-Z\s]"
        preserved_string = re.sub(pattern, "", input_string)
        return preserved_string

    def download_by_storage_id(self, storage_id: int, target_local_file_path: str) -> None:
        """Downlaods file from S3 to the local computer using only storage id

        Args:
            storage_id int: Row number to get information from storage_table
        """
        result = self.select_one_tuple_by_column_and_value(
            select_clause_value="created_user_id, path, filename", column_value=storage_id)
        if not result:
            raise ValueError(f"Storage ID {storage_id} not found in the database")
        profile_id, folder, filename = result
        self.s3.download_file(folder + filename, target_local_file_path)

    def download(self, *, file_type_id: int, remote_filename: str, local_path: str) -> None:
        """Downlaods file from S3 to local computer

        Args:
            file_type_id int: 1 - Profile Image
                                2 - Coverage Image
                                3 - Personal Introduction Video
                                4 - Scanned Diving License 
                                5 - Scanned Passport
            filename string: file name include extension, i.e.test.txt
            local_path string: where to save the file, include file extension,
            i.e.path/to/file/downloaded_test.txt
        """
        folder_and_region = self._get_region_and_folder_by_file_type_id(file_type_id)
        remote_file_path = folder_and_region[0] + '/' + remote_filename
        self.s3.download_file(remote_file_path, local_path)

    def save_image_in_storage_by_url(self, image_url: str, local_file_path: str, profile_id: int, file_type_id: int) -> None:
        self.logger.start(object={'image_url': image_url, 'local_file_path': local_file_path, 'profile_id': profile_id,
                                  'file_type_id': file_type_id})
        folder_and_region = self._get_region_and_folder_by_file_type_id(file_type_id)
        remote_file_path = folder_and_region[0] + '/'
        response = requests.get(image_url, stream=True)

        # Check if the image was retrieved successfully
        if response.status_code == requests.codes.ok:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            response.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(local_file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

            self.s3.upload_file(local_file_path=local_file_path, remote_path=remote_file_path,
                                url=image_url)
            os.remove(local_file_path)
            self.logger.end('Image successfully downloaded to ' + local_file_path)
        else:
            self.logger.error('Image couldn\'t be retrieved')

    '''
    # Not tested yet
    # TODO: later we may want to save also the html content of the url in the storage
    def download_html(self, url, local_file_path: str) -> requests.models.Response:
        METHOD_NAME = 'download_html'
        self.logger.start(METHOD_NAME, object={'url': url, 'local_file_path': local_file_path})
        response = requests.get(url)
        response.raise_for_status()
        with open(local_file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        self.logger.end(METHOD_NAME, object={'response': response})
        return response

    # TODO: maybe we shall name it save_html_in_storage_by_url
    def save_url_in_storage(self, url: str, file_type_id: int, local_file_path: str) -> int:
        METHOD_NAME = 'save_url_in_storage'
        self.logger.start(METHOD_NAME, object={'url': url, 'file_type_id': file_type_id, 'local_file_path': local_file_path})
        folder_and_region = self._get_region_and_folder_by_file_type_id(file_type_id)
        remote_file_path = folder_and_region[0] + '/'
        response = self.download_html(url, local_file_path)
        if response.status_code == requests.codes.ok:
            self.logger.info(log_message=METHOD_NAME + ': ' + 'File downloaded successfully',
                             object={'url': url, 'local_file_path': local_file_path})
            storage_id = self.s3.upload_file(local_file_path=local_file_path, remote_path=remote_file_path,
                                             url=url)
        else:
            self.logger.warning(log_message=METHOD_NAME + ': ' + 'File could not be downloaded',
                                object={'url': url, 'local_file_path': local_file_path})
            storage_id = None
        self.logger.end(METHOD_NAME, object={'storage_id': storage_id})
        return storage_id
    '''

    # TODO: later we may want to save also the html content of the url in the storage
    def save_url_in_storage(self, url: str, file_name: str) -> int:
        METHOD_NAME = 'save_url_in_storage'
        self.logger.start(METHOD_NAME, object={'url': url, 'file_name': file_name})
        script_directory = os.path.dirname(os.path.abspath(__file__))
        local_file_path = os.path.join(script_directory, file_name)
        folder_and_region = ["Url", AWS_DEFAULT_REGION]
        remote_file_path = folder_and_region[0] + '/'
        # Create a txt file with the url as it's content
        with open(local_file_path, 'w', encoding='utf-8') as file:
            file.write(url)
        storage_id = self.s3.upload_file(local_file_path=local_file_path, remote_path=remote_file_path,
                                         url=url)
        # Delete local file
        os.remove(local_file_path)
        self.logger.end(METHOD_NAME, object={'storage_id': storage_id})
        return storage_id
