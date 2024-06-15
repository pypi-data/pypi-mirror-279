# Abstract Base Classes (abc)
from abc import ABC, abstractmethod
from logger_local.MetaLogger import ABCMetaLogger


# Interface for all storage services


class StorageInterface(ABC, metaclass=ABCMetaLogger):
    """
    Method uploads a file from local_path to the cloud in remoth_path, and names the file filname
    """

    @abstractmethod
    def upload_file(self, *, local_file_path: str, remote_path: str, url: str = None) -> int or None:
        pass

    @abstractmethod
    def download_file(self, *, remote_path: str, local_path: str) -> None:
        pass

    @abstractmethod
    def delete(self, *, remote_path: str, filename: str) -> None:
        pass
