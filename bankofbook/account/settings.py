# -*- coding: utf-8 -*-
import os
from bankofbook.settings import MEDIA_ROOT

UPLOAD_AVATAR_UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'upload/account/avatar_original/')
UPLOAD_AVATAR_AVATAR_ROOT = os.path.join(MEDIA_ROOT, 'upload/account/avatar_cropped/')
UPLOAD_AVATAR_URL_PREFIX_ORIGINAL = '/static/upload/account/avatar_original/'
UPLOAD_AVATAR_URL_PREFIX_CROPPED = '/static/upload/account/avatar_cropped/'

UPLOAD_AVATAR_RESIZE_SIZE = [90, 100, 160]

if not os.path.isdir(UPLOAD_AVATAR_UPLOAD_ROOT):
	os.makedirs(UPLOAD_AVATAR_UPLOAD_ROOT)
if not os.path.isdir(UPLOAD_AVATAR_AVATAR_ROOT):
	os.makedirs(UPLOAD_AVATAR_AVATAR_ROOT)


# Default max allowed size is 3MB
UPLOAD_AVATAR_MAX_SIZE = [1024 * 1024 *3]


# Avatar default size which will be shown in you website,
# this is for call user.get_avatar_path(), user.get_avatar_url() more convenient
UPLOAD_AVATAR_DEFAULT_SIZE = [100]

# Avatar format, you can also choose: jpep, gif...
UPLOAD_AVATAR_SAVE_FORMAT = ('png')
if UPLOAD_AVATAR_SAVE_FORMAT == 'jpg':
	UPLOAD_AVATAR_SAVE_FORMAT = 'jpeg'

UPLOAD_AVATAR_SAVE_QUALITY = [100]

# Bellow settings are for web layout and text shown in web or javascript alert
UPLOAD_AVATAR_WEB_LAYOUT = {
	'crop_avatar_area_size': 300,

	'preview_areas': [
		{
			'size': 60,
			'text': '60*60像素'
		},
		{
			'size': 100,
			'text': '100*100像素'
		},
		{
			'size': 160,
			'text': '160*160像素'
		},
	]
}

UPLOAD_AVATAR_TEXT = {
	'CHOOSE_IMAGE': '选择头像',
	'CROP_IMAGE': '保存',
	'INVALID_IMAGE': '不合法文件，请选择图片',
	'NO_IMAGE': '请上传图片',
	'TOO_LARGE': '图片太大，请选择小于3M的图片',
	'ERROR': '有误，请稍后再试',
}