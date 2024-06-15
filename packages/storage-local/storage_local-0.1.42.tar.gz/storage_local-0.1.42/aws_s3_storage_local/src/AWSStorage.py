import os

import boto3
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import our_get_env

from .StorageConstants import STORAGE_TYPE_ID, FILE_TYPE_ID, EXTENSION_ID, LOGGER_CODE_OBJECT
from .StorageDB import StorageDB
from .StorageInterface import StorageInterface

AWS_ACCESS_KEY_ID = our_get_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = our_get_env("AWS_SECRET_ACCESS_KEY")


class AwsS3Storage(StorageInterface, metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):

    def __init__(self, bucket_name: str, region: str) -> None:
        self.region = region
        self.bucket_name = bucket_name
        self.storage_database = StorageDB()
        # TODO self.boto3_client
        self.client = boto3.client('s3',
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    @staticmethod
    # TODO Move this method out of this class
    def get_filename_from_path(path: str) -> str:
        return os.path.basename(path)

    def upload_file(self, *, local_file_path: str, remote_path: str, url: str = None) -> int or None:
        """uploads file to S3"""
        read_binary = 'rb'
        filename = self.get_filename_from_path(local_file_path)
        with open(local_file_path, read_binary) as file_obj:
            file_contents = file_obj.read()

        # Upload the file to S3 with the CRC32 checksum
        response = self.client.put_object(
            Bucket=self.bucket_name,
            Key=remote_path + filename,
            Body=file_contents,
            ChecksumAlgorithm='crc32'
        )
        if 'ETag' in response:
            # TODO: constracts should be replaced with parameters
            storage_id = self.storage_database.upload_to_database(file_path=remote_path, filename=filename,
                                                                  region=self.region, storage_type_id=STORAGE_TYPE_ID,
                                                                  file_type_id=FILE_TYPE_ID, extension_id=EXTENSION_ID,
                                                                  url=url)
            return storage_id
        return None

    # download a file from s3 to local_file_path
    def download_file(self, remote_path: str, local_file_path: str) -> None:
        self.client.download_file(self.bucket_name, remote_path, local_file_path)

    # logical delete
    # TODO Rename to delete_by_remote_path_filename()  [should we change the interface?]
    # TODO Make sure we have we also have delete_by_storage_id() 
    def delete(self, remote_path: str, filename: str) -> None:
        self.storage_database.delete(remote_path=remote_path, filename=filename, region=self.region)
