import os
from typing import Optional

import boto3
import cv2
import obs

from .decorator import args_log
from .loggings import logger

SUFFIX_GIF = ".gif"
SUFFIX_WEBP = "webp"
SUFFIX_jfif = "jfif"


class ObjectStorage(object):
    def __init__(self, app_config, common_struct, exception_struct):
        self.app_config = app_config
        self.common_struct = common_struct
        self.exception_struct = exception_struct

        self.path_dict = common_struct.OBJECT_STORAGE_PATHS
        self.path_dict_temp = common_struct.OBJECT_STORAGE_PATHS_TEMP
        self.allow_file_size_dict = common_struct.OBJECT_STORAGE_ALLOW_FILE_SIZE
        self.allow_file_size_default = (
            common_struct.OBJECT_STORAGE_ALLOW_FILE_SIZE_DEFAULT)
        self.file_format_whitelist = (
            common_struct.OBJECT_STORAGE_FILE_FORMAT_WHITELIST)

        self.bucket_obs = app_config.get("obs/bucket")
        self.bucket_s3 = app_config.get("s3/bucket")

        self.path_prefix_obs = app_config.get("obs/path-prefix")
        self.path_prefix_s3 = app_config.get("s3/path-prefix")

        self.base_url_obs = app_config.get("obs/base-url")
        self.base_url_s3 = app_config.get("s3/base-url")

        self.base_url_raw_obs = app_config.get("obs/base-url-raw")
        self.base_url_raw_s3 = app_config.get("s3/base-url-raw")

        self.video_base_url_obs = app_config.get("obs/video-base-url")
        self.video_base_url_s3 = app_config.get("s3/video-base-url")

        self.content_type = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "png": "image/png",
            "ico": "image/x-icon",
            "pdf": "application/pdf",
            "doc": ("application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"),
            "docx": ("application/vnd.openxmlformats-officedocument."
                     "wordprocessingml.document"),
            "mp4": "video/mp4",
            "xls": "application/vnd.ms-excel",
            "xlsx": ("application/vnd.openxmlformats-officedocument."
                     "spreadsheetml.sheet"),
            "txt": "text/plain",
            "json": "application/json",
            "xml": "text/xml"
        }

    @property
    def client_s3(self):
        return boto3.client(
            's3', region_name=self.app_config.get("s3/region"),
            aws_access_key_id=self.app_config.get("s3/key"),
            aws_secret_access_key=self.app_config.get("s3/secret"))

    @property
    def client_obs(self):
        return obs.ObsClient(
            access_key_id=self.app_config.get("obs/access_key_id"),
            secret_access_key=self.app_config.get("obs/secret_access_key"),
            server=self.app_config.get("obs/server_url"))

    def parse_file_key_of_obs(self, url):
        return url.replace(
            self.base_url_obs.replace("{file}", ""), "").replace(
                self.base_url_raw_obs.replace("{file}", ""), "")

    def parse_file_key_of_s3(self, url):
        return url.replace(
            self.base_url_s3.replace("{file}", ""), "").replace(
                self.base_url_raw_s3.replace("{file}", ""), "")

    @args_log()
    def parse_file_key(self, system, url):
        return {
            self.common_struct.OBJECT_STORAGE_SYSTEM.OBS: (
                self.parse_file_key_of_obs),
            self.common_struct.OBJECT_STORAGE_SYSTEM.S3: (
                self.parse_file_key_of_s3)
        }[system](url)

    @args_log()
    def _check_resource_file(
            self, resource_name, file_name, binary_content=None):
        if resource_name not in list(self.path_dict.keys()):
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg="The resource name is invalid.")
        # 验证文件类型
        file_format = file_name.split(".")[-1]
        allow_file_format = self.file_format_whitelist.get(resource_name, ())
        if not file_name or file_format not in allow_file_format:
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg="This file type is not supported.")
        if not binary_content:
            return
        # 验证文件大小
        allow_file_size = self.allow_file_size_dict.get(
            resource_name, self.allow_file_size_default)
        content_size = float(len(binary_content)) / 1024**2
        if content_size > allow_file_size:
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg="The file size is too large.")

    @args_log()
    def _get_video_screenshot_bytes(self, video_name):
        vc = cv2.VideoCapture(video_name)  # pylint: disable=no-member
        if not vc.isOpened():
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg="Not a qualified video file.")
        frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))  # pylint: disable=no-member
        # fps = vc.get(cv2.CAP_PROP_FPS)  # 视频帧率
        # duration = frames / fps  # 视频时长
        if frames < 10:
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg="Not a qualified video file.")
        currentframe = 1
        while True:
            res, frame = vc.read()
            if res:
                if currentframe == 10:  # 取第10帧图片
                    _, jpeg = cv2.imencode('.jpg', frame)
                    jb = jpeg.tobytes()
                    vc.release()
                    return jb
                currentframe += 1
            else:
                break
        vc.release()

    @args_log()
    def upload_file_to_obs(
            self, path, file_name, binary_content, path_kargs=None):
        try:
            # 填充路径前缀, 填充路径参数
            if path_kargs is not None:
                path = path.format(prefix=self.path_prefix_obs, **path_kargs)
            else:
                path = path.format(prefix=self.path_prefix_obs)
            name_suffix = file_name.split('.')[-1].lower()
            _object_key = "{}/{}".format(path, file_name)
            _object_url = self.base_url_raw_obs.format(file=_object_key)
            _headers = obs.PutObjectHeader(
                contentType=self.content_type[name_suffix]
            )
            self.client_obs.putContent(
                self.bucket_obs, _object_key, content=binary_content,
                headers=_headers)
        except Exception as err:
            logger.exception(err)
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg=str(err))
        return {"objectKey": _object_key, "objectUrl": _object_url}

    @args_log()
    def upload_file_to_s3(
            self, path, file_name, binary_content=None, path_kargs=None):
        try:
            # 填充路径前缀, 填充路径参数
            if path_kargs is not None:
                path = path.format(prefix=self.path_prefix_s3, **path_kargs)
            else:
                path = path.format(prefix=self.path_prefix_s3)
            name_suffix = file_name.split('.')[-1].lower()
            _object_key = "{}/{}".format(path, file_name)
            _object_url = self.base_url_raw_s3.format(file=_object_key)
            resp = self.client_s3.put_object(
                Bucket=self.bucket_s3, Key=_object_key,
                Body=binary_content, ContentType=self.content_type[name_suffix])
            print(resp)
        except Exception as err:
            logger.exception(err)
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg=str(err))
        return {"objectKey": _object_key, "objectUrl": _object_url}

    @args_log()
    def upload_file(
            self, system, resource_name, file_name, binary_content,
            is_temp=None, path_kargs=None):
        # 统一将文件名小写
        file_name = file_name.lower()
        # 检查文件类型
        self._check_resource_file(resource_name, file_name, binary_content)
        # 判断是否临时文件
        if is_temp is True:
            path = self.path_dict_temp.get(resource_name)
            if not path:
                raise self.exception_struct.InvalidOperationException(
                    code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                    msg="未配置临时文件路径, 请联系管理.")
        else:
            path = self.path_dict.get(resource_name)

        # 根据system参数不同选择不同的上传方法
        upload_method = {
            self.common_struct.OBJECT_STORAGE_SYSTEM.OBS: (
                self.upload_file_to_obs),
            self.common_struct.OBJECT_STORAGE_SYSTEM.S3: (
                self.upload_file_to_s3)
        }[system]
        result = upload_method(path, file_name, binary_content, path_kargs)

        _object_url = result["objectUrl"]
        # 如果是视频, 存视频展示图
        if resource_name.find('video') != -1:
            video_img = self._get_video_screenshot_bytes(_object_url)
            try:
                upload_method(
                    path=path,
                    file_name='{}{}'.format(file_name.split('.')[0], '.jpg'),
                    binary_content=video_img, path_kargs=path_kargs)
            except Exception as err:
                logger.exception(err)
                raise self.exception_struct.InvalidOperationException(
                    code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                    msg=str(err))
        return result

    @args_log()
    def confirm_temp_file_in_obs(self, resource, temp_obj_key, path_kargs=None):
        # 如果temp_obj_key是http开头的, 直接返回
        temp_obj_key = self.parse_file_key_of_obs(temp_obj_key)
        if temp_obj_key.startswith("http"):
            # 判断是否S3文件
            if temp_obj_key != self.parse_file_key_of_s3(temp_obj_key):
                raise self.exception_struct.InvalidOperationException(
                    code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                    msg="Invalid file.")
            return temp_obj_key
        # 处理文件在临时目录和正式目录的路径
        temp_path = self.path_dict_temp.get(resource)
        path = self.path_dict.get(resource)
        if path_kargs is not None:
            temp_path = temp_path.format(
                prefix=self.path_prefix_obs, **path_kargs)
            path = path.format(
                prefix=self.path_prefix_obs, **path_kargs)
        else:
            temp_path = temp_path.format(prefix=self.path_prefix_obs)
            path = path.format(prefix=self.path_prefix_obs)
        obj_key = temp_obj_key.replace(temp_path, path)
        # 检测文件在正式目录是否存在, 若存在则直接返回
        res = self.client_obs.getObjectMetadata(self.bucket_obs, obj_key)
        if res.status == 200:
            return obj_key
        # 从临时目录复制一份到正式目录
        resp = self.client_obs.copyObject(
            sourceBucketName=self.bucket_obs, sourceObjectKey=temp_obj_key,
            destBucketName=self.bucket_obs, destObjectKey=obj_key)
        if resp.status >= 300:
            logger.error(str(resp))
            raise self.exception_struct.InvalidOperationException(
                code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                msg=str(resp.reason))
        # 如果是视频, 转存视频展示图
        if resource.find('video') != -1:
            temp_video_img_obj_key = temp_obj_key.replace("mp4", "jpg")
            video_img_obj_key = obj_key.replace("mp4", "jpg")
            resp = self.client_obs.copyObject(
                sourceBucketName=self.bucket_obs,
                sourceObjectKey=temp_video_img_obj_key,
                destBucketName=self.bucket_obs,
                destObjectKey=video_img_obj_key)
            if resp.status >= 300:
                logger.error(str(resp))
                raise self.exception_struct.InvalidOperationException(
                    code=self.exception_struct.CODE_UPLOAD_FILE_FAILED,
                    msg=str(resp.reason))
        return obj_key

    @args_log()
    def confirm_temp_file_in_s3(self, resource, temp_obj_key, path_kargs=None):
        # 如果temp_obj_key是http开头的, 直接返回
        temp_obj_key = self.parse_file_key_of_s3(temp_obj_key)
        if temp_obj_key.startswith("http"):
            return temp_obj_key
        return self.confirm_temp_file_in_obs(resource, temp_obj_key, path_kargs)

    @args_log()
    def confirm_temp_file(
            self, system, resource, temp_obj_key, path_kargs=None):
        confirm_temp_file_mmthod = {
            self.common_struct.OBJECT_STORAGE_SYSTEM.OBS: (
                self.confirm_temp_file_in_obs),
            self.common_struct.OBJECT_STORAGE_SYSTEM.S3: (
                self.confirm_temp_file_in_s3)
        }[system]
        try:
            return confirm_temp_file_mmthod(resource, temp_obj_key, path_kargs)
        except Exception:
            return temp_obj_key

    @args_log()
    def resize(self, url, size):
        # 暂时前端处理了
        return url

    @args_log()
    def format_and_resize(self, image: str, size: Optional[int] = None):
        if not image or SUFFIX_WEBP in image or SUFFIX_jfif in image:
            return image
        ext_info = os.path.splitext(image)
        suffix = ext_info[-1]
        # 如图片为gif不做处理即可
        if suffix and suffix.lower() == SUFFIX_GIF:
            return image
        if size:
            image = f"{image}?x-image-process=image/format,webp/resize,w_{size}#"
        else:
            image = f"{image}?x-image-process=image/format,webp#"
        return image

    @args_log()
    def get_file_url(self, file, resource=None, size=None, system=None):
        if not file or file.startswith("http"):
            return file
        # 如果存储的不是完整的路径, 则需要根据resource拼接完整的路径
        if resource is not None and system is not None:
            path = self.path_dict[resource]
            file = "{}/{}".format(path, file)
            if system == self.common_struct.OBJECT_STORAGE_SYSTEM.OBS:
                file = file.format(prefix=self.path_prefix_obs)
            elif system == self.common_struct.OBJECT_STORAGE_SYSTEM.S3:
                file = file.format(prefix=self.path_prefix_s3)
        # 根据前缀判断文件是存储华为的OBS还是亚马逊的S3
        if file.startswith(self.app_config.get("obs/path-prefix")):
            if file.endswith(".mp4"):
                url = self.app_config.get(
                    "obs/video-base-url").format(file=file)
            else:
                url = self.app_config.get("obs/base-url").format(file=file)
        else:
            if file.endswith(".mp4"):
                url = self.app_config.get(
                    "s3/video-base-url").format(file=file)
            else:
                url = self.app_config.get("s3/base-url").format(file=file)
        # 拼接图片的查询参数
        # 华为的OBS支持根据查询参数返回压缩或裁剪后的图片
        if size is not None:
            url = self.resize(url, size)
        return url

    @args_log()
    def get_file_urls(self, files, resource=None, size=None, system=None):
        return [self.get_file_url(file, resource, size, system)
                for file in files if file] if files else []
