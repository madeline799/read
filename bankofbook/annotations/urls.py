from django.conf.urls import patterns, url

from annotations import views


urlpatterns = patterns('',
	url(r'^(?P<an_id>[^\.]+)$', views.annotation, name='annotation'),
)



