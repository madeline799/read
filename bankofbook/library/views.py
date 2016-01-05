import os
import re
import uuid

import datetime
import jwt

from django.db.models import  Model, Q
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from bankofbook import settings

from library.forms import SearchForm
from library.models import (Lcc, Book, Booklcc, Author, ViewCategory,
							ViewBooklist, Bookcover, UserBooklist,
							UserBooklistCurrent)


dummyapp  = "bookstore/gtb/"
dummyappcover = "bookstore/gtb.cover/"

# Create your views here.
def index(request):
	return category(request, 'Hotest')

def category(request, categorycode=None):
	lccclass 	= None
	lccsubclass = None

	book_list = None
	lccdescription = None

	lcctrue = 1
	firstPage = 1
	lastPage = 1

	lccclass = ViewCategory.objects.filter(is_subclass=0)
	lccsubclass = ViewCategory.objects.filter(is_subclass=1).filter(book_id__isnull=False)

	if request.method == 'GET':
		lcc = request.GET.get('lcc',None)
		searchkeywords = request.GET.get('keywords',None)

		if lcc == None:
			lcc = categorycode

		if lcc == 'Hotest':
			book_list = ViewBooklist.objects.values('id','cover','title','first_names','last_name').distinct().filter(cover__isnull=False).order_by('-downloads')			
			lcctrue = 0

		elif lcc == 'Latest':
			book_list = ViewBooklist.objects.values('id','cover','title','first_names','last_name').distinct().filter(cover__isnull=False).order_by('-id')
			lcctrue = 0

		elif lcc == "Search":
			book_list = ViewBooklist.objects.values('id','cover','title','first_names','last_name').distinct().filter(Q(title__icontains=searchkeywords) | Q(first_names__icontains=searchkeywords) | Q(last_name__icontains=searchkeywords)).order_by('-downloads')
			lcctrue = 0

		else:
			book_list = ViewBooklist.objects.filter( lcc = lcc)
			
			lccdescription = Lcc.objects.get(lcc=lcc, is_subclass=1).description_cn

		paginator = Paginator(list(book_list), 16)

		page = request.GET.get('page',1)

		if int(page) - 5 > 0:
			rangePaginatorPrev = paginator.page_range[int(page)-5:int(page)-1]
			rangePaginatorNext = paginator.page_range[int(page):int(page)+5]
			firstPage = int(page) - 4
		else:
			rangePaginatorPrev = paginator.page_range[0:int(page)-1]
			rangePaginatorNext = paginator.page_range[int(page):int(page)+5]

		lastPage = int(page) + 6

		try:
			bookinfos = paginator.page(page)
		except PageNotAnInteger:
			bookinfos = paginator.page(1)
		except EmptyPage:
			bookinfos = paginator.page(paginator.num_pages)

		return render(request, 'library/category.html', {
			'lcc': lcc,
			'lccclass': lccclass,
			'lccsubclass': lccsubclass,
			'lccdes': lccdescription,
			'bookinfos': bookinfos,
			'bookcoverpath': dummyappcover,
			'searchkeywords': searchkeywords,
			'lcctrue': lcctrue,
			'rangePaginatorPrev': rangePaginatorPrev,
			'rangePaginatorNext': rangePaginatorNext,
			'paginator': paginator,
			'firstPage': firstPage,
			'lastPage': lastPage,
		})

def book(request, booknumber):

	bookdigit = None
	bookdownloadpath = ''

	if request.method == 'GET':
		book_id = request.GET.get('lcc',None)
		if book_id == None:
			book_id = booknumber

		bookdetails = Book.objects.raw('''
			select a.*, b.*
			from library_book as a
			inner join library_author as b on a.author_id = b.id
			where a.id = %s''',[book_id])

		lccdetails = Lcc.objects.raw('''
			select *
			from library_booklcc
			where book_id = %s''', [book_id])

		lcshdetails = Lcc.objects.raw('''
			select *
			from library_booklcsh
			where book_id = %s''', [book_id])

		bookcovers = Bookcover.objects.filter(book_id=book_id).filter(cover__isnull=False).order_by('-vote')[0:5]

		book = Book.objects.get(id=book_id)

		bookdigit = list(book_id)

		for digit in bookdigit:
			bookdownloadpath = bookdownloadpath + '/' + digit

		bookdownloadpath = bookdownloadpath[1:2*len(bookdigit)-1]
		bookdownloadpath = bookdownloadpath + book_id + '/' + book_id + '-h.zip'

	return render(request, 'library/book.html', {
		'bookdetails': bookdetails,
		'lccdetails': lccdetails,
		'lcshdetails': lcshdetails,
		'book': book,
		'bookdownloadpath': bookdownloadpath,
		'bookcovers': bookcovers,
		'bookcoverpath': dummyappcover,
	})

@csrf_exempt
def bookhtml(request, booknumber=10047):

	bookdigit = None 
	contents = None
	bookindex = ''

	offset = 0

	templatestring = ''
	currentbook = None
	
	#store reading progress only in POST mode
	if request.method == 'POST':
		book_id = request.POST.get('booknumber',None)
		if book_id == None:
			book_id = booknumber

		offset = str(request.POST['offset'])
		print offset
		#print typeof(offset)
		if request.user.is_authenticated():
			try:
				item = UserBooklist.objects.get(user=request.user,book_id=book_id)
				if item:
					item.position = offset
					item.save()
			except:
				item = UserBooklist(book_id=book_id, user=request.user, position=offset)
				item.save()

			try:
				itemCurrent = UserBooklistCurrent.objects.get(user=request.user)
				if itemCurrent:
					itemCurrent.book_id = book_id
					itemCurrent.save()
			except:
				itemCurrent = UserBooklistCurrent(book_id=book_id, user=request.user)
				itemCurrent.save()

			#print "is_authenticated"
		else:
			#print "no_authenticated"
			pass
	elif request.method == 'GET':
		book_id = request.GET.get('booknumber',None)
		if book_id == None:
			book_id = booknumber

		if request.user.is_authenticated():
			try:
				item = UserBooklist.objects.get(user=request.user,book_id=book_id)
				if item:
					offset = item.position;
			except:
				pass
		else:
			pass

		bookdigit = list(book_id)

		if len(bookdigit) ==1:
			bookfolder = "0/"+book_id +'/'
		else:
			for digit in bookdigit:
				bookindex = bookindex + '/' + digit
			bookfolder = bookindex[1:2*len(bookdigit)-1]+book_id +'/'
		
		bookfoldertext0 = bookfolder + book_id + '-0.txt'
		bookfoldertext8 = bookfolder + book_id + '-8.txt'
		bookfolderhtml  = bookfolder + book_id + '-h/'+ book_id + '-h.htm'
		bookfolderhtmlimage = bookfolder + book_id + '-h/images'

		bookistext=False
		for templatedir in settings.TEMPLATE_DIRS:
			print templatedir
			if os.path.isfile(templatedir+dummyapp+bookfolderhtml):
				templatestring = templatedir+dummyapp+bookfolderhtml
				break
			elif os.path.isfile(templatedir+dummyapp+bookfoldertext0):
				templatestring = templatedir+dummyapp+bookfoldertext0
				bookistext =True
				break
			elif os.path.isfile(templatedir+dummyapp+bookfoldertext8):
				templatestring = templatedir+dummyapp+bookfoldertext8
				bookistext =True
				break

		if templatestring:
			templatestring = open(templatestring).read()

		if bookistext:
			templatestring = templatestring.replace('\n','\n<br>')

		codestring = 'Character set encoding: '
		if templatestring:
			codestring_pos_start = templatestring.find(codestring)+len(codestring)
			codestring_pos_end   = templatestring.find('\n', codestring_pos_start)
			code = templatestring[codestring_pos_start:codestring_pos_end].strip()

		if templatestring:
			templatestring = templatestring.decode(code)
			templatestring = templatestring.replace('src="images'
					,' class="img-responsive" '+'data-layzr="/static/' + dummyapp + bookfolderhtmlimage)

			book_start = templatestring.find  ( '</pre>', templatestring.find("START OF THIS PROJECT GUTENBERG") ) +len("</pre>")
			book_end   = templatestring.rfind ( '<pre' , 0, templatestring.find("END OF THIS PROJECT GUTENBERG") )

			templatestring = templatestring[ book_start : book_end ]

		if not templatestring:
			currentbook = Book.objects.get(id=book_id)

		repattern0 = re.compile(r'<li>.*[\n]*</li>') #54
		repattern1 = re.compile(r'<a[\s]*.*href="#[a-zA-Z].*".*</a>') #19
		repattern2 = re.compile(r'<a[\s]*href="#[_A-Z].*".*</a>') #10085
		repattern3 = re.compile(r'<a[\s]*href="#[0-9]{1,2}".*</a>') #310066
		repattern4 = re.compile(r'<a[\s]*href="#[0-9]*[\-][0-9]*".*[\n]*.*</a>') #10008
		repattern5 = re.compile(r'<a[\s]*href="#[\w]*[\_]*"[\n]*.*[\n]*.*[\n]*</a>') #10038
		repattern6 = re.compile(r'<A[\s]*HREF="#[\w]*[\_]*".*[\n]*.*</A>') #1001

		contents0 = repattern0.findall(templatestring)
		contents1 = repattern1.findall(templatestring)
		contents2 = repattern2.findall(templatestring)
		contents3 = repattern3.findall(templatestring)
		contents4 = repattern4.findall(templatestring)
		contents5 = repattern5.findall(templatestring)
		contents6 = repattern6.findall(templatestring)

		if contents0:
			contents = contents0
		elif contents1:
			contents = contents1
		elif contents2:
			contents = contents2
		elif contents3:
			contents = contents3
		elif contents4:
			contents = contents4
		elif contents5:
			contents = contents5
		elif contents6:
			contents = contents6


	return render(request, 'library/bookhtml.html', {
		'offset': offset,
		'templatestring': templatestring,
		'contents': contents,
		'currentbook': currentbook,
		'booknumber': book_id,
	})

def search(request):
	if request.method == "GET":
		form = SearchForm(request.GET)

		if form.is_valid():
			return category(request, 'Search')
		else:
			# NOT hit, valition  done using bootstrap method 
			pass


# Replace these with your details
CONSUMER_KEY = 'annotateit'
CONSUMER_SECRET = str(uuid.uuid5(uuid.NAMESPACE_DNS, CONSUMER_KEY))

# Only change this if you're sure you know what you're doing
CONSUMER_TTL = 86400
def generate_token(request,userid=None):
	return HttpResponse(
		jwt.encode(
			{'consumerKey': CONSUMER_KEY,
			'userId': userid,
			'issuedAt': _now().isoformat() + 'Z',
			'ttl': CONSUMER_TTL},
			CONSUMER_SECRET
		)
	)

def _now():
	return datetime.datetime.utcnow().replace(microsecond=0)
