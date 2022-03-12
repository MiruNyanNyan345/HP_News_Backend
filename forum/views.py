from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Posts
from .serializer import PostMakeSerializer, PostVoteSerializer, ReplyMakeSerializer, ReplyVoteSerializer, \
    PostsGetSerializer


# Get all Posts
class GetPosts(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # First post come first
        allPosts = Posts.objects.all().order_by("-datetime")
        serializer = PostsGetSerializer(allPosts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Make a Post
class MakePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostMakeSerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            post = serializer.save()
            if post:
                return Response("Made Post!!!", status=status.HTTP_201_CREATED)
            else:
                return Response("Make-Post Failed!", status=status.HTTP_400_BAD_REQUEST)


# Vote Post
class VotePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostVoteSerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            vote = serializer.save()
            if vote:
                return Response("Vote Successfully!!!", status=status.HTTP_201_CREATED)
            else:
                return Response("Vote Failed!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Post's Reply
class ReplyPost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReplyMakeSerializer(data=request.data, user=request.user)

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
        serializer = ReplyVoteSerializer(data=request.data, user=request.user)

        if serializer.is_valid():
            vote = serializer.save()
            if vote:
                return Response("Vote for reply successfully!!!", status=status.HTTP_201_CREATED)
            else:
                return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
