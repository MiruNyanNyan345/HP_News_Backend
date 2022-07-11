from datetime import datetime

from rest_framework import serializers
from rest_framework.response import Response

from .models import Posts, PostVotes, Replies, ReplyVotes, SavePost
from account.models import CustomUser


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class GetPostsVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVotes
        fields = ("post_id", "vote")


class GetPostsSerializer(serializers.ModelSerializer):
    post_votes = GetPostsVotesSerializer(read_only=True, many=True)
    author = GetUserSerializer()
    isSaved = serializers.BooleanField()

    class Meta:
        model = Posts
        fields = ("id", "title", "body", "author", "datetime", "post_votes", 'isSaved')
        depth = 1


class MakePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(MakePostSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        instance = self.Meta.model(title=validated_data["title"],
                                   body=validated_data["body"],
                                   author_id=self.user.id,
                                   # datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                   )
        instance.save()
        print("Made Post Instance:\nID: {} \n{}".format(instance.id, instance))

        return instance


class VotePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVotes
        fields = ("post", "vote")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(VotePostSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        user = self.user
        post_id = data.pop("post", None).id
        if self.Meta.model.objects.filter(user_id=user.id, post_id=post_id):
            raise serializers.ValidationError({'Vote Error': "You have voted this post!!!"})
        data["user_id"] = self.user.id
        data["post_id"] = post_id
        return data

    def create(self, validated_data):
        vote = validated_data.pop("vote", None)
        post_id = validated_data.pop("post_id", None)
        user_id = validated_data.pop("user_id", None)

        instance = self.Meta.model(post_id=post_id,
                                   user_id=user_id,
                                   vote=vote)
        print("Post-Vote Instance:\n", instance)
        instance.save()
        return instance


class ReplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Replies
        fields = ('post', 'body')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ReplyPostSerializer, self).__init__(*args, **kwargs)

    def create(self, data):
        author_id = self.user.id
        post_id = data.pop("post", None).id
        body = data.pop("body", None)

        instance = self.Meta.model(post_id=post_id,
                                   body=body,
                                   author_id=author_id)
        instance.save()
        print("Made Reply Instance:\nID: {} \n{}".format(instance.id, instance))

        return instance


class GetRepliesVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyVotes
        fields = ("reply_id", "vote")


class GetRepliesSerializer(serializers.ModelSerializer):
    reply_votes = GetRepliesVotesSerializer(read_only=True, many=True)
    author = GetUserSerializer()

    class Meta:
        model = Posts
        fields = ("id", "body", "author", "datetime", "reply_votes")
        depth = 1


class VoteReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyVotes
        fields = ("reply", "vote")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(VoteReplySerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        user_id = self.user.id
        reply_id = data.pop("reply", None).id
        if self.Meta.model.objects.filter(user_id=user_id, reply_id=reply_id):
            raise serializers.ValidationError({"vote_error": "You have voted this reply!!!"})
        data["user_id"] = user_id
        data["reply_id"] = reply_id
        return data

    def create(self, validated_data):
        reply_id = validated_data.pop("reply_id", None)
        vote = validated_data.pop("vote", None)
        user_id = validated_data.pop("user_id", None)

        instance = self.Meta.model(
            reply_id=reply_id,
            vote=vote,
            user_id=user_id
        )
        instance.save()
        print("Reply-Vote Instance:\n", instance)

        return instance


class SavePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePost
        fields = ('post',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(SavePostSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        user_id = self.user.id
        post_id = data.pop("post", None).id
        data['user_id'] = user_id
        data['post_id'] = post_id
        return data

    def create(self, validated_data):
        post_id = validated_data.pop("post_id", None)
        user_id = validated_data.pop("user_id", None)

        instance = self.Meta.model(post_id=post_id, user_id=user_id)
        if self.Meta.model.objects.filter(user_id=user_id, post_id=post_id):
            t = self.Meta.model.objects.filter(user_id=user_id, post_id=post_id).first()
            t.delete()
            print("Unsaved Post Instance:\n{}".format(instance))
            return False
        else:
            instance.save()
            print("Save Post Instance:\n{}".format(instance))
            return True
