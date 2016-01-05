from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from account.forms import UserForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from library.models import UserBooklist, UserBooklistCurrent
from account.models import UserUploadAvatar

from django.utils.crypto import get_random_string

import os
import hashlib
import time

from PIL import Image
from account.signals import avatar_crop_done
from django.core.exceptions import ObjectDoesNotExist

from account.settings import (
	UPLOAD_AVATAR_MAX_SIZE,
	UPLOAD_AVATAR_UPLOAD_ROOT,
	UPLOAD_AVATAR_AVATAR_ROOT,
	UPLOAD_AVATAR_URL_PREFIX_ORIGINAL,
	UPLOAD_AVATAR_RESIZE_SIZE,
	UPLOAD_AVATAR_SAVE_FORMAT,
	UPLOAD_AVATAR_SAVE_QUALITY,
	UPLOAD_AVATAR_WEB_LAYOUT,
	UPLOAD_AVATAR_TEXT,
)

border_size = UPLOAD_AVATAR_WEB_LAYOUT['crop_avatar_area_size']

def signUp(request):
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			registered = True

		else:
			print user_form.errors

	else:
		user_form = UserForm()

		return render_to_response('account/signup.html', {}, context)

	return render_to_response(
			'account/signin.html',
			{'user_form': user_form, 'registered': registered},
			context)

def signIn(request, booknumber=None):
	context = RequestContext(request)

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				if booknumber and booknumber != 'None':
					return HttpResponseRedirect(reverse('library:bookhtml', args=(booknumber,)))
				else:
					return HttpResponseRedirect(reverse('account:user', args=(user.id,)))
			else:
				return HttpResponse("Your account is disabled.")
		else:
			print "Invaild login details:{0},{1}"
			return HttpResponse("Invaild login details supplied")
	else:
		return render_to_response('account/signin.html', {}, context)

@login_required
def signOut(request):
	logout(request)

	return HttpResponseRedirect('/library/')

def get_upload_avatar_context():

	upload_avatar_context = UPLOAD_AVATAR_WEB_LAYOUT.copy()
	upload_avatar_context.update(UPLOAD_AVATAR_TEXT)
	return upload_avatar_context

@login_required
def user(request, uid):
	user_id = None
	avatar_src = None

	if request.method == 'GET':
		user_id = request.GET.get('uid',None)

	if user_id == None:
		user_id = uid

	readinglist = UserBooklist.objects.raw('''
			select distinct b.id, b.title, a.position
			from library_user_booklist as a
			inner join library_view_booklist as b on a.book_id = b.id
			where a.user_id = %s''',user_id)

	try:
		userbooklistcurrent = UserBooklistCurrent.objects.get(user_id=user_id)
	except:
		userbooklistcurrent = None

	user = User.objects.get(id=uid)

	client = Elasticsearch('amango.org:9200')
	s = Search(using=client, index="annotateit") \
		.query("match", user=user.username)

	response = s.execute()

	try:
		u = UserUploadAvatar.objects.get(user_id=request.user.id, isCurrent=1)
		if u:
			avatar_src = u.get_avatar_url(100)
	except UserUploadAvatar.DoesNotExist:
		pass

	return render(request, 'account/profile.html', {
		'user': request.user,
		'readinglist': readinglist,
		'userbooklistcurrent': userbooklistcurrent,
		'annotation': response,
		'avatarsrc': avatar_src,
	})

@login_required
def uploadAvatar(request):
	context = RequestContext(request)

	request.session['uploadAvatar'] = request.META.get('HTTP_REFERER', '/')

	return render_to_response(
		'account/uploadavatar.html',
		get_upload_avatar_context(),
		context_instance = context
	)

class UploadAvatarError(Exception):
	pass

@login_required
def uploadedAvatar(request):
	try:
		uploaded_file = request.FILES['uploadAvatarFile']
	except KeyError:
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['INVALID_IMAGE'])

	if uploaded_file.size > UPLOAD_AVATAR_MAX_SIZE:
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['TOO_LARGE'])

	name, ext = os.path.splitext(uploaded_file.name)
	new_name = hashlib.md5(
		'%s%f' % (get_random_string(), time.time())
	).hexdigest()
	new_name = '%s%s' % (new_name, ext.lower())
	avatar_name, _ = os.path.splitext(new_name)

	fpath = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, new_name)

	with open(fpath, 'wb') as f:
		for c in uploaded_file.chunks(10240):
			f.write(c)

	try:
		Image.open(fpath)
	except IOError:
		try:
			os.unlink(fpath)
		except:
			pass
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['INVALID_IMAGE'])

	try:
		upload_avatar = UserUploadAvatar.objects.get(user_id=request.user.id, isCurrent=1)
		if upload_avatar:
			upload_avatar.isCurrent = 0
			upload_avatar.save()
			upload_avatar_new = UserUploadAvatar(user_id=request.user.id, avatar_original=new_name, avatar_name=avatar_name, isCurrent=1)
			upload_avatar_new.save()
	except ObjectDoesNotExist:
		upload_avatar = UserUploadAvatar(user_id=request.user.id, avatar_original=new_name, avatar_name=avatar_name, isCurrent=1)
		upload_avatar.save()

	return HttpResponse(
		"<script>window.parent.upload_avatar_success('%s')</script>" % \
		(UPLOAD_AVATAR_URL_PREFIX_ORIGINAL + new_name)
	)

@login_required
def uploadedCrop(request):
	context = RequestContext(request)

	try:
		upload_avatar = UserUploadAvatar.objects.get(user_id=request.user.id, isCurrent=1)
	except UserUploadAvatar.DoesNotExist:
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['NO_IMAGE'])
	image_orig = upload_avatar.get_avatar_original_path()

	if not image_orig:
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['NO_IMAGE'])

	try:
		x1 = int(float(request.POST['x1']))
		y1 = int(float(request.POST['y1']))
		x2 = int(float(request.POST['x2']))
		y2 = int(float(request.POST['y2']))
	except:
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['ERROR'])

	try:
		orig = Image.open(image_orig)
	except IOError:
		raise UploadAvatarError(UPLOAD_AVATAR_TEXT['NO_IMAGE'])

	orig_w, orig_h = orig.size
	if orig_w <= border_size and orig_h <= border_size:
		ratio = 1
	else:
		if orig_w > orig_h:
			ratio = float(orig_w) / border_size
		else:
			ratio = float(orig_h) / border_size
	box = [int(x * ratio) for x in [x1, y1, x2, y2]]
	avatar = orig.crop(box)
	avatar_name, _ = os.path.splitext(upload_avatar.avatar_original)

	def _resize(size):
		res = avatar.resize((size, size), Image.ANTIALIAS)
		res_name = '%s-%d.%s' % (avatar_name, size, UPLOAD_AVATAR_SAVE_FORMAT)
		res_path = os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, res_name)
		res.save(res_path, UPLOAD_AVATAR_SAVE_FORMAT, quality=UPLOAD_AVATAR_SAVE_QUALITY)

	for size in UPLOAD_AVATAR_RESIZE_SIZE:
		_resize(size)

	upload_avatar.avatar_cropped_coordinate = box
	upload_avatar.save()

	avatar_crop_done.send(sender=None, user_id=request.user.id, avatar_original=upload_avatar.avatar_original, avatar_name=avatar_name, avatar_cropped_coordinate=box, isCurrent=1)

	return HttpResponseRedirect(request.session['uploadAvatar'])