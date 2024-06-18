from .base_abstract import PyCloudFS
from .base_exceptions import *

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError as BotoClientError

class aws_s3(PyCloudFS):
    def __init__(self, access_key, secret_key) -> None:
        self.client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    def list_files(self, bucket, limit=10, **kwargs):
        try:
            response = self.client.list_objects_v2(Bucket=bucket, MaxKeys=limit, **kwargs)
            return [(res['Key'], res['Size']) for res in response['Contents']]
        except BotoClientError as e:
            raise NoBucketFound(f'No bucket found with name {bucket}')
        
    def check_file_exists(self, bucket, filename) -> bool:
        try:
            self.client.head_object(Bucket=bucket, Key=filename)
            return True
        except BotoClientError as e:
            return False
        
    def download_file(self, bucket, filename, localpath, **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            try:
                local_filename = localpath + "/" + filename.split("/")[-1]  
                with open(local_filename, 'wb') as f:
                    self.client.download_fileobj(Bucket=bucket, Key=filename, Fileobj=f, **kwargs)
                return local_filename
            except Exception as e:
                raise GeneralException(e)
        else:
            raise FileNotFoundException()
        
    def upload_file(self, bucket, filename, localpath, **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            raise FileAlreadyExists()
        else:
            try:
                with open(localpath, 'rb') as f:
                    self.client.upload_fileobj(Fileobj=f, Bucket=bucket, Key=filename, **kwargs)
                return filename
            except BotoClientError as e:
                raise GeneralException(e)
            
    def multipart_upload_file(self, bucket, filepath, local_filepath, chunk_size=10485760, **kwargs) -> str:
        config = TransferConfig(multipart_threshold=chunk_size, max_concurrency=3)
        self.upload_file(bucket=bucket, filename=filepath, localpath=local_filepath, Config=config, **kwargs)

            
    def delete_file(self, bucket, filename, **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            try:
                self.client.delete_object(Bucket=bucket, Key=filename)
                return filename
            except BotoClientError as e:
                raise GeneralException(e)
        else:
            raise FileNotFoundException()
        
    def presigned_url(self, bucket, filename, expiration=3600,  **kwargs) -> str:
        if self.check_file_exists(bucket, filename):
            try:
                return self.client.generate_presigned_url(ClientMethod = 'get_object',
                                                            Params={'Bucket': bucket, 'Key': filename}, 
                                                            ExpiresIn=expiration,
                                                            **kwargs)
            except BotoClientError as e:
                raise GeneralException(e)
        else:
            raise FileNotFoundException()
        
    def presigned_url_upload(self, bucket, filename, local_filepath, expiration=3600, **kwargs) -> str:
        try:
            self.upload_file(bucket, filename, local_filepath)
            return self.presigned_url(bucket, filename, expiration, **kwargs)
        except Exception as e:
            raise GeneralException(e)
        
    def copy_file_bucket(self, source_bucket, destination_bucket, source_filepath, destination_filepath,**kwargs) -> bool:
        if self.check_file_exists(source_bucket, source_bucket):
            try:
                self.client.copy_object(Bucket=destination_bucket, Key=destination_filepath, CopySource={'Bucket': source_bucket, 'Key': source_filepath})
                return True
            except BotoClientError as e:
                raise GeneralException(e)
            finally:
                return False
        else:
            raise FileNotFoundException()