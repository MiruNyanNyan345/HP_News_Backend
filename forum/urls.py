from django.urls import path
from .views import MakePost, VotePost, ReplyPost, VoteReply

urlpatterns = [
    path('post/make/', MakePost.as_view(), name='make_post'),
    path('post/vote/', VotePost.as_view(), name='vote_post'),
    path('post/reply/', ReplyPost.as_view(), name='reply_post'),
    path('post/vote_reply/', VoteReply.as_view(), name='reply_post'),
]
