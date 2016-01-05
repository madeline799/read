from django.conf.urls import patterns, url

from account import views


urlpatterns = patterns('',
	url(r'^signin/(?P<booknumber>[\w\t]{0,5})$', views.signIn, name='signin'),
	url(r'^signup/$', views.signUp, name='signup'),
	url(r'^signout/$', views.signOut, name='signout'),
	url(r'^user/(?P<uid>[0-9]{1,14})$', views.user, name='user'),
	url(r'^uploadAvatar/$', views.uploadAvatar, name='uploadAvatar'),
	url(r'^uploadedAvatar/?$', views.uploadedAvatar, name="uploadedAvatar"),
	url(r'^uploadedCrop/?$', views.uploadedCrop, name="uploadedCrop"),

)
