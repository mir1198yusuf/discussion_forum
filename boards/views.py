from django.shortcuts import render, get_object_or_404, redirect
from boards.models import Board,Post,Topic
from forms_dir.newtopic_form import NewTopic_Form
from forms_dir.topicreply_form import TopicReply_Form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from forms_dir.postedit_form import PostEdit_Form
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max, Count
from django.urls import reverse
from django.conf import settings

# Create your views here.

#home class based view using generic class views 
class Home_View(ListView):
	allow_empty = True #if no boards 
	context_object_name = 'boards'
	model = Board
	template_name = 'homepage.html'
	paginate_by = settings.BOARD_PAGINATE_BY
	
	def get_queryset(self):
		#for home page, boards will be ordered by last updated
		queryset = Board.objects.all()
		#annotate last updated on
		queryset = queryset.annotate(lastupdated_on=Max('topics__posts__updated_on'))
		#annotate post count
		queryset = queryset.annotate(posts_count=Count('topics__posts'))
		##in future to get entire post object pass this date and topic to Post model and get
		#order by last updated descending
		queryset = queryset.order_by('-lastupdated_on')
		return queryset

#board topics page function
def board_topics(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	#we will sort topics on last updated post in descending
	queryset = board.topics.all().annotate(lastupdated_on=Max('posts__updated_on'))
	#add replies count column - -1 because 1st post is not a reply
	queryset = queryset.annotate(replies_count=Count('posts')-1)
	queryset = queryset.order_by('-lastupdated_on')	
	#request.GET is dict of get parameters
	page = request.GET.get(key='page', default=1)	#first time page will not be there in url, so use 1
	paginator = Paginator(queryset, settings.TOPIC_PAGINATE_BY)
	try:
		topics = paginator.page(page)
	except PageNotAnInteger:	#if page is not a valid integer
		#fallback to 1st page
		topics = paginator.page(1)
	except EmptyPage:	#valid page no but page no doesnot exists
		#fallback to last page
		topics = paginator.page(paginator.num_pages)
		#since we are using reusable template for pagination, we need to pass 4 things in template context
		##we can do this view also with generic CBV, but for learning pagination better,we are keeping this as FBV
		#4 things are : page_obj, paginator, is_paginated, object_list -> though we are using only 3 in reusable pagination template
	return render(request, 'boardtopicpage.html', {'board': board, 'topics': topics, 'paginator':paginator, 'page_obj':topics, 'object_list':topics.object_list, 'is_paginated':topics.has_other_pages()})

#new topic page function
@login_required()	#login needed to create new topic
def new_topic(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	if request.method=='POST':	#if POST request ie submit button was clicked
		user = request.user 	#get currently logged in user
		form = NewTopic_Form(request.POST) #request.POST contains data submitted through POST request
		if form.is_valid():	#if form data has no errors
			#Create the Topic
			topic = form.save(commit=False)	#create a Topic model DB instance but dont save the instance since we have to do some edits
			#subject already added in topic instance since topic model was defined in Meta class of form
			#we will add board and created_by values
			topic.board = board 
			topic.created_by = user
			topic.save()
			#Now create the Post object in DB 
			Post.objects.create(message=form.cleaned_data.get('message'), topic=topic, created_by=user)
			return redirect('topic_page_url', board_id=board.id, topic_id=topic.id)	
	elif request.method=='GET':
		form = NewTopic_Form()	#blank form
	return render(request, 'newtopicpage.html', {'board':board, 'form':form})

#topic page class based view using generic list view
class TopicPage_View(ListView):
	allow_empty = True
	context_object_name = 'posts'
	model = Post
	ordering = 'id'	
	#the above ordering is related to get_pageno_of_post() of Topic model
	#if needed to change, change at both places
	paginate_by = settings.POST_PAGINATE_BY
	template_name = 'topicpage.html'

	def dispatch(self,request, *args, **kwargs):
		#self.kwargs is the values in url. stays throughout the class
		#though kwargs==self.kwargs , kwargs is self.kwargs False
		self.board = get_object_or_404(Board, id=self.kwargs.get('board_id'))
		self.topic = get_object_or_404(Topic, id=self.kwargs.get('topic_id'))
		#create session key for topic view - to increase views of topic only once per user per session
		session_key = 'viewed_topic_id_{}'.format(self.topic.id)
		if not request.session.get(session_key, default=False):	#if True-session_key not set
			request.session[session_key] = True 	#set session_key
			#increase the views count of topic
			self.topic.views += 1
			self.topic.save()	#save changes in DB
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(topic=self.topic)

	def get_context_data(self, **kwargs):
		#add board and topic to template context
		kwargs['board'] = self.board
		kwargs['topic'] = self.topic 
		return super().get_context_data(**kwargs)

#topic reply page
@login_required() #login needed to create new reply post
def topic_reply_page(request,board_id,topic_id):
	board = get_object_or_404(Board, id=board_id)
	topic = get_object_or_404(Topic, id=topic_id)
	if request.method == 'POST':
		form = TopicReply_Form(request.POST)
		if form.is_valid():
			#save post in db and return to topic page
			post = form.save(commit=False)
			post.topic = topic 	#get current topic
			post.created_by = request.user 	#get currently logged in user
			post.save()
			#finding page number of new post in topic page
			pageno = topic.get_last_posts_pageno()
			topicurl = reverse('topic_page_url', kwargs={'board_id':board.id, 'topic_id':topic.id})
			return redirect('{url}?page={pageno}#{postid}'.format(url=topicurl, pageno=pageno, postid=post.id), board_id=board.id, topic_id=topic.id)
	elif request.method == 'GET':
		form = TopicReply_Form()
	return render(request, 'topicreplypage.html',{'board':board, 'topic':topic, 'form':form})

#post edit class based view using generic view UpdateView
@method_decorator(login_required, name='dispatch')	#login needed to edit post
class PostEdit_View(UpdateView):
	context_object_name = 'post'	#the post object which will be identified by post_id in url and updated in db
	form_class = PostEdit_Form 	#form class
	model = Post 	#model to update object of.
	template_name = 'posteditpage.html'	#html file name
	pk_url_kwarg = 'post_id'	#argument of url to use to identify object of model mentioned

	def dispatch(self, request, *args, **kwargs):
		#self.kwargs = url argument dictionary
		##extracts board id and topic id from url 
		self.board = get_object_or_404(Board, id=self.kwargs.get('board_id'))	
		self.topic = get_object_or_404(Topic, id=self.kwargs.get('topic_id'))
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		kwargs['board'] = self.board
		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		#allow editing of self created post because with correct url anyone can edit anyones post
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)	#created_by=logged in user

	#success url attribute not defined because form_valid redirects to success_url but since we have overriden it, we will redirect as well
	def form_valid(self,form):
		#this is called in post auto. so need to check request method is POST
		post = form.save(commit=False)
		#topic already added
		#also created_by/created_on will remain same
		post.updated_on = timezone.now()
		post.save()
		#we have to redirect user to same topic page where this post was after editing save
		topicpageurl = reverse('topic_page_url', kwargs={'board_id':self.board.id, 'topic_id':self.topic.id})
		pageno = self.topic.get_pageno_of_post(post)
		newtopicurl_pageid = '{url}?page={pageno}#{postid}'.format(url=topicpageurl, pageno=pageno, postid=post.id)
		return redirect(newtopicurl_pageid)


