from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'bankofbook.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^opds/', include('opds.urls', namespace='opds')),
	url(r'^library/', include('library.urls', namespace='library')),
	url(r'^account/', include('account.urls', namespace='account')),
	url(r'^annotations/', include('annotations.urls', namespace='annotations')),

	url(r'^$', include('library.urls', namespace='library')),
)
