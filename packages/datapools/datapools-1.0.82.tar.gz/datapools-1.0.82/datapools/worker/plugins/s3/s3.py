import os
import io
import tempfile
import traceback
from typing import Callable

import boto3

from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError

from ....common.logger import logger
from ....common.types import CrawlerContent
from ..base_plugin import BasePlugin, BasePluginException, BaseReader
from ...worker import WorkerTask


class S3Reader(BaseReader):

    def __init__(self, s3_client, bucket_name, key):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.key = key

    async def read_to(self, f: io.IOBase, __stopper: Callable):  # TODO: use stopper
        self.s3_client.download_fileobj(self.bucket_name, self.key, f)


class S3Exception(BasePluginException):
    pass


class S3Plugin(BasePlugin):
    def __init__(self, ctx, aws_access_key_id=None, aws_secret_access_key=None):
        super().__init__(ctx)

        if aws_access_key_id is None:
            logger.info("getting aws_access_key_id from env")
            aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        if aws_secret_access_key is None:
            logger.info("getting aws_secret_access_key from env")
            aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        logger.info(f"{aws_access_key_id=}")
        logger.info(f"{aws_secret_access_key=}")

        # empty key means bucket is public
        if aws_access_key_id == "":
            self.is_public_bucket = True
            self.s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
            self.s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
        else:
            self.is_public_bucket = False
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            self.s3 = boto3.resource(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.info( f'============ s3 {u=} =====================================')
        if u.netloc == "s3.console.aws.amazon.com":
            # logger.info( 'netloc ok')
            if u.path[0:12] == "/s3/buckets/":
                # logger.info( 'path ok')
                return True
            # elif u.path[0:6] == '/watch' and u.query[0:2] == 'v=':
            #     self.video_id = u.query[2:13]
            #     return True

        return False

    async def process(self, task: WorkerTask):
        logger.info(f"s3::process({task.url})")

        u = self.parse_url(task.url)
        self.bucket_name = u.path.split("/")[3]
        logger.info(f"{self.bucket_name=}")

        bucket = self.s3.Bucket(self.bucket_name)

        try:
            copyright_tag_id = self._download(BasePlugin.license_filename)
            copyright_tag = await BasePlugin.parse_tag_in(copyright_tag_id.decode())
            logger.info(f"found license: {copyright_tag_id}")
        except S3Exception:
            logger.error("bucket does not contain license.txt, cannot process(1)")
            logger.error(traceback.format_exc())
            return
        except ClientError:
            logger.error("bucket does not contain license.txt, cannot process(2)")
            logger.error(traceback.format_exc())
            return

        for obj in bucket.objects.all():
            logger.info(f"{obj=}")

            if obj.key == BasePlugin.license_filename:
                continue

            if self.is_public_bucket is False:
                # THIS IS PURE API ACCESS URL
                obj_url = f"https://s3.console.aws.amazon.com/s3/buckets/{self.bucket_name}/{obj.key}"
            else:
                # THIS IS DIRECT URL ( FOR PUBLIC BUCKETS )
                # TODO: region?
                obj_url = f"https://{self.bucket_name}.s3.amazonaws.com/{obj.key}"

            # storage_id = self.ctx.storage.gen_id(obj_url)

            # content = self._download(obj.key)

            try:
                # content_type = self._get_datapool_content_type(content)
                # content_type = BasePlugin.get_content_type_by_content(content)

                # tag = None
                # if content_type == DatapoolContentType.Image:
                #     tag = BasePlugin.parse_image_tag(content)

                # if tag is None and copyright_tag is None:
                #     continue

                # await self.ctx.storage.put(storage_id, content)

                yield CrawlerContent(
                    # tag_id=str(tag) if tag is not None else None,
                    # tag_keepout=tag.is_keepout() if tag is not None else False,
                    copyright_tag_id=str(copyright_tag) if copyright_tag is not None else None,
                    copyright_tag_keepout=copyright_tag.is_keepout() if copyright_tag is not None else False,
                    # type=content_type,
                    # storage_id=storage_id,
                    url=obj_url,
                    # content=content,
                    content=S3Reader(self.s3_client, self.bucket_name, obj.key),
                )
            except S3Exception as e:
                logger.info(f"mime type not supported/detected: {e}")

    def _download(self, key):
        with tempfile.NamedTemporaryFile() as tmp:
            self.s3_client.download_fileobj(self.bucket_name, key, tmp)

            tmp.seek(0, 0)
            return tmp.read()

    # def _get_datapool_content_type(self, content):
    #     type = filetype.guess(content)
    #     if type is None:
    #         raise S3Exception("unknown file type")
    #     return BasePlugin.get_content_type_by_mime_type(type.mime)
