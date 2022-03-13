from datetime import datetime

from rest_framework import serializers

from .models import Posts, PostVotes, Replies, ReplyVoteCount


class GetPostsVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVotes
        fields = ("post_id", "vote")


class GetPostsSerializer(serializers.ModelSerializer):
    post_votes = GetPostsVotesSerializer(read_only=True, many=True)

    class Meta:
        model = Posts
        fields = ("id", "title", "body", "author", "datetime", "post_votes")
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
            raise serializers.ValidationError({"vote_error": "You have voted this post!!!"})
        data["user_id"] = self.user.id
        data["post_id"] = post_id
        return data

    def create(self, validated_data):
        print(validated_data)
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


class VoteReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyVoteCount
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
