from django.urls import path
from .views import MakePost, VotePost

urlpatterns = [
    path('post/make/', MakePost.as_view(), name='make_post'),
    path('post/vote/', VotePost.as_view(), name='vote_post')
]
