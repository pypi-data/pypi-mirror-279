from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .StorageConstants import LOGGER_CODE_OBJECT


class StorageDB(GenericCRUD, metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):
    def __init__(self) -> None:
        super().__init__(default_schema_name='storage', default_table_name='storage_table',
                         default_view_table_name='storage_view', default_column_name='storage_id')

    def upload_to_database(self, *, file_path: str, filename: str, region: str, storage_type_id: int, file_type_id: int,
                           extension_id: int, url: str = None) -> int:
        data_dict = {"path": file_path, "filename": filename, "region": region, "url": url,
                     "storage_type_id": storage_type_id, "file_type_id": file_type_id,
                     "file_extension_id": extension_id}
        storage_id = self.insert(data_dict=data_dict)
        return storage_id

    def delete(self, *, remote_path: str, filename: str, region: str) -> int:
        where = "path = %s AND filename = %s AND region = %s"
        params = (remote_path, filename, region)
        storage_id = super().select_one_value_by_where(where=where, params=params, select_clause_value="storage_id")
        super().delete_by_where(where=where, params=params)
        return storage_id
