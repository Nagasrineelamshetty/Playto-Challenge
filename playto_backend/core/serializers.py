from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


# =========================
# User Serializer
# =========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# =========================
# Post Serializer
# =========================
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'created_at',
            'like_count'
        ]


# =========================
# Comment Serializer
# =========================
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    parent = serializers.IntegerField(source='parent.id', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'content',
            'created_at',
            'parent',
            'like_count'
        ]


# =========================
# Like Input Serializer
# =========================
class LikeSerializer(serializers.Serializer):
    """
    This serializer validates intent.
    The actual Post/Comment resolution happens in the view.
    """
    target_type = serializers.ChoiceField(choices=['post', 'comment'])
    target_id = serializers.IntegerField()
