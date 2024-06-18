from abc import ABC, abstractmethod

class PyCloudFS(ABC):
    @abstractmethod
    def list_files(self, bucket, limit=10, **kwargs) -> list:
        # List files in bucket
        # Parameter 
        #       bucket: str
        #       limit: int
        #       kwargs: dict
        # Return 
        #       tuple of (name, size)
        # Size is in bytes and name is a string
        pass

    @abstractmethod
    def check_file_exists(self, bucket, filename) -> bool:
        # Check for a single file in a bucket
        # Parameter
        #       bucket: str
        #       filename: str   (filename in bucket which can include path name like media/xyz.jpg)
        # Return
        #       bool
        pass

    @abstractmethod
    def download_file(self, bucket, filename, localpath, **kwargs) -> str:
        # Download a single file from a bucket
        # Parameter
        #       bucket: str 
        #       filename: str   (filename in bucket which can include path name like media/xyz.jpg)
        #       localpath: str  (path to local folder in which file will be downloaded not filename)
        #       kwargs: dict
        # Return
        #       str (file path in local)
        pass

    @abstractmethod
    def upload_file(self, bucket, filepath, local_filepath, **kwargs) -> str:
        # Upload a single file to a bucket
        # Parameter
        #       bucket: str
        #       filepath: str           (filename in bucket which can include path name like media/xyz.jpg)
        #       local_filepath: str     (path to local file from which file will be uploaded)
        #       kwargs: dict
        # Return
        #       str (filename in bucket)
        pass

    @abstractmethod
    def multipart_upload_file(self, bucket, filepath, local_filepath, chunk_size=10485760, **kwargs) -> str:
        # Upload a single file to a bucket using multipart upload
        # Parameter
        #       bucket: str
        #       filepath: str           (filename in bucket which can include path name like media/xyz.jpg)
        #       local_filepath: str     (path to local file from which file will be uploaded)
        #       chunk_size: int          (in bytes, default is 10MB)
        #       kwargs: dict
        # Return
        #       str (filename in bucket)
        pass

    @abstractmethod
    def delete_file(self, bucket, filename, **kwargs) -> str:
        # Delete a single file from a bucket
        # Parameter
        #       bucket: str
        #       filename: str   (filename in bucket which can include path name like media/xyz.jpg)
        # Return
        #       str (deleted filename in bucket)
        pass

    @abstractmethod
    def presigned_url(self, bucket, filename, expiration=3600, **kwargs) -> str:
        # Generate a presigned url for a single file for GET method
        # Parameter
        #       bucket: str
        #       filename: str       (filename in bucket which can include path name like media/xyz.jpg)
        #       expiration: int     (in seconds)
        # Return
        #       str (presigned url)
        pass

    @abstractmethod
    def presigned_url_upload(self, bucket, filepath, local_filepath, expiration=3600,  **kwargs) -> str:
        # Generate a presigned url for a single file for GET method after uploading file to bucket
        # Parameter
        #       bucket: str
        #       filepath: str           (filename in bucket which can include path name like media/xyz.jpg)
        #       local_filepath: str     (path to local file from which file will be uploaded)
        #       expiration: int         (in seconds)
        # Return
        #       str (presigned url)
        pass

    @abstractmethod
    def copy_file_bucket(self, source_bucket, destination_bucket, source_filepath, destination_filepath, **kwargs) -> bool:
        # Copy a single file from one bucket to another
        # Parameter
        #       source_bucket: str
        #       destination_bucket: str
        #       source_filepath: str        (Filepath in source bucket)
        #       destination_filepath: str   (Filepath in destination bucket)
        # Return
        #       bool
        pass