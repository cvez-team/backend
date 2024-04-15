import uuid
import time
from ..configs.firebase_config import bucket
from ..utils.logger import log_firebase


class StorageProvider:
    '''
    A provider class to handle the storage of files.
    '''

    def __init__(self, directory: str) -> None:
        self.directory = directory

    def __get_ref(self, filename: str) -> str:
        '''
        Get the reference of the file in the storage.
        '''
        file_base_name = filename.split(".")[0]
        file_extension = filename.split(".")[-1]
        filename = f"{file_base_name}_{uuid.uuid4().hex[:5]}.{file_extension}"
        return f"{self.directory}/{filename}"

    def upload(self, file: bytes, filename: str, content_type: str) -> tuple[str, str]:
        '''
        Upload the file to the storage.
        Return the file path and the public URL of the file.
        '''
        path = self.__get_ref(filename.replace(" ", "_"))

        _s = time.perf_counter()
        blob = bucket.blob(path)
        _e = time.perf_counter() - _s

        log_firebase(f"Storage upload to {path} [{_e:.2f}s]")

        blob.upload_from_string(file, content_type)
        blob.make_public()
        return path, blob.public_url

    def download(self, path: str) -> bytes:
        '''
        Download the file from the storage.
        '''
        blob = bucket.blob(path)

        _s = time.perf_counter()
        data = blob.download_as_bytes()
        _e = time.perf_counter() - _s

        log_firebase(f"Storage download from {path} [{_e:.2f}s]")

        return data

    def remove(self, path: str) -> None:
        '''
        Remove the file from the storage.
        '''
        blob = bucket.blob(path)

        _s = time.perf_counter()
        blob.delete()
        _e = time.perf_counter() - _s

        log_firebase(f"Storage delete from {path} [{_e:.2f}s]")
