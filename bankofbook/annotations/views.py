from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

def annotation(request, an_id=None):


	client = Elasticsearch('amango.org:9200')

	s = Search(using=client, index="annotateit") \
		.query("match", id=an_id)


	response = s.execute()

	for hit in response:
		print (hit.to_dict())
		#return HttpResponse(hit.to_dict())


		return render(request, 'annotations/annotation.html', {
		'annotate': hit.to_dict(),
	})


