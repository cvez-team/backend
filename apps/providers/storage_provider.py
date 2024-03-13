import uuid
from ..configs.firebase_config import bucket


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

    def upload(self, file: bytes, filename: str) -> tuple[str, str]:
        '''
        Upload the file to the storage.
        Return the file path and the public URL of the file.
        '''
        path = self.__get_ref(filename.replace(" ", "_"))
        blob = bucket.blob(path)
        blob.upload_from_string(file)
        return path, blob.public_url

    def download(self, path: str) -> bytes:
        '''
        Download the file from the storage.
        '''
        blob = bucket.blob(path)
        return blob.download_as_bytes()
