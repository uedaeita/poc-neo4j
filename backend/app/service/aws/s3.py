import logging
from io import TextIOWrapper

import boto3

from app.core.config import Settings

logger = logging.getLogger(__name__)


class S3:
    def __init__(self):
        self.client = boto3.client("s3", endpoint_url=Settings.S3_ENDPOINT)

    def upload_fileobj(self, fileobj: TextIOWrapper, bucket: str, key: str) -> bool:
        try:
            self.client.upload_fileobj(fileobj, bucket, key)
            return True
        except Exception as e:
            logger.error(e)
            return False


s3 = S3()
