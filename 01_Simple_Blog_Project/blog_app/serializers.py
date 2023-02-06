from rest_framework import serializers
from blog_app.models import Post, Upvote, Comment


class PostSerializer(serializers.ModelSerializer):
    #user = serializers.HiddenField(source='user.username')
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created', 'updated', 'user', 'upvote_count')
        read_only_fields = ('id',)
        #extra_kwargs = {'user':{'read_only':True}}


class UpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ('id', 'user', 'post')
        read_only_fields = ('id', 'user')


class CommentSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'body')
        read_only_fields = ('id',)