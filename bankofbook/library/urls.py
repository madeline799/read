from django.conf.urls import patterns, url

from library import views


urlpatterns = patterns('',
	url(r'^book/html/(?P<booknumber>[0-9]{1,5})$', views.bookhtml, name='bookhtml'),
	url(r'^book/(?P<booknumber>[0-9]{1,5})$', views.book, name='book'),
	url(r'^category/(?P<categorycode>[A-Z]{1}[a-zA-Z0-9/\-.]{0,9})$', views.category, name='category'),
	url(r'^generate_token/(?P<userid>[\w]{4,18})$', views.generate_token, name='generate_token'),
	url(r'^search/$', views.search, name='search'),
	url(r'^$', views.index, name='index'),
)
