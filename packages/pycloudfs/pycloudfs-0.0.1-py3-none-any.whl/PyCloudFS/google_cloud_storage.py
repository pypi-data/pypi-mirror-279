from .base_abstract import PyCloudFS
from .base_exceptions import *
 
from google.cloud import storage
from google.cloud.storage import transfer_manager

class gcp_storage(PyCloudFS):
    def __init__(self) -> None:
        # Login will be done through -gcloud init commmand API key is restricted
        try:
            self.client = storage.Client()
        except Exception as e:
            if e.__class__.__name__ == 'DefaultCredentialsError':
                raise NoCredentialsFound('No credentials found')
            else:
                raise e

    def list_files(self, bucket, limit=10, **kwargs) -> list:
        try:
            blobs = self.client.list_blobs(bucket_or_name=bucket, max_results=limit, **kwargs)
            return [(blob.name, blob.size) for blob in blobs]
        except Exception as e:
            raise NoBucketFound(f'No bucket found with name {bucket}')
        
    def check_file_exists(self, bucket, filename) -> bool:
        try:
            return self.client.bucket(bucket_name=bucket).blob(blob_name=filename).exists()
        except Exception as e:
            raise NoBucketFound(f'No bucket found with name {bucket}')
        
    def download_file(self, bucket, filename, localpath, **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            try:
                blob = self.client.bucket(bucket_name=bucket).blob(blob_name=filename)
                local_filename = localpath + "/" + filename.split("/")[-1]  
                with open(local_filename, 'wb') as f:
                    blob.download_to_file(file_obj=f)
                return local_filename
            except Exception as e:
                raise GeneralException(e)
        else:
            raise FileNotFoundException()
        
    def upload_file(self, bucket, filepath, local_filepath, **kwargs) -> bool:
        if self.check_file_exists(bucket, filepath):
            raise FileAlreadyExists()
        else:
            try:
                blob = self.client.bucket(bucket_name=bucket).blob(blob_name=filepath)
                with open(local_filepath, 'rb') as f:
                    blob.upload_from_file(file_obj=f)
                return bucket
            except Exception as e:
                raise GeneralException(e)
            
    def multipart_upload_file(self, bucket, filepath, local_filepath, chunk_size=10485760, **kwargs) -> str:
        if self.check_file_exists(bucket, filepath):
            raise FileAlreadyExists()
        else:
            try:
                blob = self.client.bucket(bucket_name=bucket).blob(blob_name=filepath)
                
                transfer_manager.upload_chunks_concurrently(
                    local_filepath, blob, chunk_size=chunk_size, max_workers=4
                )
            except Exception as e:
                raise GeneralException(e)
            
    def delete_file(self, bucket, filename, **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            try:
                blob = self.client.bucket(bucket_name=bucket).blob(blob_name=filename)
                blob.delete()
                return filename
            except Exception as e:
                raise GeneralException(e)
        else:
            raise FileNotFoundException()
        
    def presigned_url(self, bucket, filename, expiration=3600, **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            try:
                blob = self.client.bucket(bucket_name=bucket).blob(blob_name=filename)
                return blob.generate_signed_url(expiration=expiration,
                                                method='GET',
                                                **kwargs)
            except Exception as e:
                raise GeneralException(e)
        else:
            raise FileNotFoundException()
        
    def presigned_url_upload(self, bucket, filename, local_filepath, expiration=3600, **kwargs) -> str:
        try:
            self.upload_file(bucket, filename, local_filepath)
            return self.presigned_url(bucket, filename, expiration, **kwargs)    
        except Exception as e:
            raise GeneralException(e)
        
    def copy_file_bucket(self, source_bucket, destination_bucket, source_filepath, destination_filepath, **kwargs) -> bool:
        if self.check_file_exists(source_bucket, source_bucket):
            try:
                source_blob = self.client.bucket(bucket_name=source_bucket).blob(blob_name=source_filepath)
                destination_blob = self.client.bucket(bucket_name=destination_bucket).blob(blob_name=destination_filepath)
                job = source_blob.rewrite(destination_blob)
                job.result()
                return True
            except Exception as e:
                raise GeneralException(e)
            finally:
                return False
        else:
            raise FileNotFoundException()