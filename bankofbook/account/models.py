import os

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_delete
from account.signals import avatar_crop_done

from account.settings import (
	UPLOAD_AVATAR_UPLOAD_ROOT,
	UPLOAD_AVATAR_AVATAR_ROOT,
	UPLOAD_AVATAR_URL_PREFIX_CROPPED,
	UPLOAD_AVATAR_SAVE_FORMAT,
	UPLOAD_AVATAR_DEFAULT_SIZE,
)
# Create your models here.

class UploadAvatarMixIn:
	"""user MUST define self.get_uid(), and self.get_avatar_name() method for using this mixin
	self.get_uid() return the current user's uid,
	self.get_avatar_name() return avatar name
	"""

	def get_uploaded_image_name(self):
		try:
			return UserUploadAvatar.objects.only('avatar_name').get(user_id=self.get_uid())
		except UserUploadAvatar.DoesNotExist:
			return None

	def get_uploaded_image_path(self):
		name = self.get_uploaded_image_name()
		if not name:
			return name

		full_path = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, name)
		if not os.path.exists(full_path):
			return None
		return full_path

	def build_avatar_name(self, name, size):
		return '%s-%d.%s' % (name, size, UPLOAD_AVATAR_SAVE_FORMAT)

	def get_avatar_path(self, size=UPLOAD_AVATAR_DEFAULT_SIZE):
		full_path = os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, self.get_avatar_name(size))
		if not os.path.exists(full_path):
			return None
		return full_path

	def get_avatar_url(self, size=UPLOAD_AVATAR_DEFAULT_SIZE):
		return UPLOAD_AVATAR_URL_PREFIX_CROPPED + self.get_avatar_name(size)

class UserUploadAvatar(models.Model, UploadAvatarMixIn):
	user = models.ForeignKey('auth.User', related_name='user_info')
	avatar_name = models.CharField(max_length=255)
	avatar_original = models.CharField(max_length=255)
	avatar_cropped_coordinate = models.CharField(max_length=255)
	upload_date = models.DateTimeField(auto_now_add=True)
	isCurrent = models.IntegerField(max_length=10)

	def get_uid(self):
		return self.user.id

	def get_avatar_name(self, size):
		return UploadAvatarMixIn.build_avatar_name(self, self.avatar_name, size)

	def get_avatar_original_path(self):
		path = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, self.avatar_original)
		if not os.path.exists(path):
			return None
		return path

	def __unicode__(self):
		return self.avatar_name

def save_avatar_in_db(sender, user_id, avatar_name, avatar_original, avatar_cropped_coordinate, isCurrent, **kwargs):
	u = UserUploadAvatar.objects.get(user_id=user_id, isCurrent=1)
	if not u:
		UserUploadAvatar.objects.create(user_id=user_id, avatar_name=avatar_name, avatar_original=avatar_original, avatar_cropped_coordinate=avatar_cropped_coordinate, isCurrent=1)


def _delete_avatar_on_disk(sender, instance, *args, **kwargs):
	path = instance.get_avatar_original_path()
	if path:
		try:
			os.unlink(path)
		except OSError:
			pass

avatar_crop_done.connect(save_avatar_in_db)
post_delete.connect(_delete_avatar_on_disk, sender=UserUploadAvatar)

