from django.db import models
from account.models import CustomUser


# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "Title: {}\nBody: {}\nCreated-By: {}\nCreated-DateTime: {}".format(
            self.title,
            self.body,
            self.author,
            self.datetime
        )

class PostVotes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="post_votes")
    vote = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Post: {}\nVote: {}\nUser: {}\nVote DateTime: {}".format(
            self.post,
            self.vote,
            self.user,
            self.datetime
        )


class Replies(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Post: {}\nBody: {}\nCreated-By: {}".format(
            self.post,
            self.body,
            self.author
        )


class ReplyVoteCount(models.Model):
    reply = models.ForeignKey(Replies, on_delete=models.CASCADE)
    vote = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Reply: {}\nVote: {}\nUser: {}\nVote DateTime: {}".format(
            self.reply,
            self.vote,
            self.user,
            self.datetime
        )