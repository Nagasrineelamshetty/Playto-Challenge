from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum, Case, When, IntegerField, F

from django.contrib.auth.models import User

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class LeaderboardAPIView(APIView):
    def get(self, request):
        since = timezone.now() - timedelta(hours=24)

        leaderboard = (
            Like.objects
            .filter(created_at__gte=since)
            .annotate(
                points=Case(
                    When(post__isnull=False, then=5),
                    When(comment__isnull=False, then=1),
                    output_field=IntegerField(),
                ),
                karma_user=Case(
                    When(post__isnull=False, then=F("post__author")),
                    When(comment__isnull=False, then=F("comment__author")),
                )
            )
            .values("karma_user")
            .annotate(total_karma=Sum("points"))
            .order_by("-total_karma")[:5]
        )

        users = User.objects.in_bulk(
            [row["karma_user"] for row in leaderboard]
        )

        response = [
            {
                "user_id": row["karma_user"],
                "username": users[row["karma_user"]].username,
                "karma": row["total_karma"],
            }
            for row in leaderboard
        ]

        return Response(response)
    
class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_type = serializer.validated_data["target_type"]
        target_id = serializer.validated_data["target_id"]
        user = request.user

        try:
            with transaction.atomic():
                if target_type == "post":
                    Like.objects.create(
                        user=user,
                        post_id=target_id
                    )
                else:
                    Like.objects.create(
                        user=user,
                        comment_id=target_id
                    )

        except IntegrityError:
            return Response(
                {"status": "already_liked"},
                status=200
            )

        return Response(
            {"status": "liked"},
            status=201
        )
def build_comment_tree(comments):
    comment_map = {}
    roots = []

    for comment in comments:
        comment.replies_list = []
        comment_map[comment.id] = comment

    for comment in comments:
        if comment.parent_id:
            parent = comment_map.get(comment.parent_id)
            if parent:
                parent.replies_list.append(comment)
        else:
            roots.append(comment)

    return roots

class PostListAPIView(APIView):
    def get(self, request):
        posts = (
            Post.objects
            .select_related("author")
            .annotate(like_count=Count("likes"))
            .order_by("-created_at")
        )

        comments = (
            Comment.objects
            .select_related("author")
            .annotate(like_count=Count("likes"))
            .order_by("created_at")
        )

        comments_by_post = {}
        for comment in comments:
            comments_by_post.setdefault(comment.post_id, []).append(comment)

        response = []

        for post in posts:
            post_comments = comments_by_post.get(post.id, [])
            tree = build_comment_tree(post_comments)

            post_data = PostSerializer(post).data
            post_data["comments"] = self.serialize_tree(tree)

            response.append(post_data)

        return Response(response)

    def serialize_tree(self, comments):
        data = []
        for comment in comments:
            serialized = CommentSerializer(comment).data
            serialized["replies"] = self.serialize_tree(comment.replies_list)
            data.append(serialized)
        return data
