from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Posts, Replies, SavePost
from .serializer import MakePostSerializer, VotePostSerializer, ReplyPostSerializer, VoteReplySerializer, \
    GetPostsSerializer, GetRepliesSerializer, SavePostSerializer


# Get all Posts and their Votes
class GetPosts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # First post come first
        posts = Posts.objects.all().order_by("-datetime")
        p_serializer = GetPostsSerializer(posts, many=True)
        return Response(p_serializer.data, status=status.HTTP_200_OK)


# Make a Post
class MakePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MakePostSerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            post = serializer.save()
            if post:
                # return Response("Made Post!!!", status=status.HTTP_201_CREATED)
                return Response({"Posted": ""}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Post Failed": ""}, status=status.HTTP_400_BAD_REQUEST)


# Vote Post
class VotePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VotePostSerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            vote = serializer.save()
            if vote:
                return Response("Vote Successfully!!!", status=status.HTTP_201_CREATED)
            else:
                return Response("Vote Failed!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get Votes of Post
class GetReplies(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        post_id = request.query_params['post_id']
        replies = Replies.objects.filter(post__replies=post_id).order_by('-datetime')
        # First Replies come first
        r_serializer = GetRepliesSerializer(replies, many=True, )
        return Response(r_serializer.data, status=status.HTTP_200_OK)


# Post's Reply
class ReplyPost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReplyPostSerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            reply = serializer.save()
            if reply:
                return Response("Submit Reply Successfully!!!", status=status.HTTP_201_CREATED)
            else:
                return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vote Reply
class VoteReply(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VoteReplySerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            vote = serializer.save()
            if vote:
                return Response("Vote for reply successfully!!!", status=status.HTTP_201_CREATED)
            else:
                return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Save Post
class SaveForumPost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SavePostSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            saved = serializer.save()
            if saved:
                return Response("Saved Post", status=status.HTTP_201_CREATED)
            else:
                return Response("Unsaved Post", status=status.HTTP_200_OK)
        else:
            return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)


# Check if request post is saved by user
class CheckPostIsSaved(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        post_id = request.query_params['post_id']
        user_id = request.user.id
        if SavePost.objects.filter(post_id=post_id, user_id=user_id).exists():
            return Response(1, status=status.HTTP_200_OK)
        else:
            return Response(0, status=status.HTTP_200_OK)


# Get all user's saved posts
class GetAllSavedPost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        savedPosts = SavePost.objects.filter(user_id=user_id).all()
        sp_objs = []
        for i in savedPosts:
            sp_objs.append(Posts.objects.get(id=i.post_id))
        serializer = GetPostsSerializer(sp_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
