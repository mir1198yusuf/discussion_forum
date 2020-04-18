from django.urls import path
import boards.views

urlpatterns = [
	path('<int:board_id>/', boards.views.board_topics, name='board_topics_url'),	#list topics for a board
	path('<int:board_id>/newtopic/', boards.views.new_topic, name='new_topic_url'),	#new topic page
	path('<int:board_id>/topic/<int:topic_id>/', boards.views.TopicPage_View.as_view(), name='topic_page_url'), #topic page
	path('<int:board_id>/topic/<int:topic_id>/reply/', boards.views.topic_reply_page, name='topic_reply_url'), #topic reply page
	path('<int:board_id>/topic/<int:topic_id>/post/<int:post_id>/edit/', boards.views.PostEdit_View.as_view(), name='post_edit_url'), #post edit url

]

