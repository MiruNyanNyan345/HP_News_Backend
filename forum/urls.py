from django.urls import path
from .views import MakePost, VotePost, ReplyPost, VoteReply, GetPosts, GetReplies, SaveForumPost, CheckPostIsSaved, \
    GetAllSavedPost

urlpatterns = [
    path('post/get_posts/', GetPosts.as_view(), name='get_posts'),
    path('post/make/', MakePost.as_view(), name='make_post'),
    path('post/vote/', VotePost.as_view(), name='vote_post'),
    path('post/get_replies/', GetReplies.as_view(), name='get_replies'),
    path('post/reply/', ReplyPost.as_view(), name='reply_post'),
    path('post/vote_reply/', VoteReply.as_view(), name='reply_post'),
    path('post/save_post/', SaveForumPost.as_view(), name='save_post'),
    path('post/post_is_saved/', CheckPostIsSaved.as_view(), name='post_is_saved'),
    path('post/get_saved_posts/', GetAllSavedPost.as_view(), name='get_saved_posts'),
]
