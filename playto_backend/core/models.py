from django.db import models
from django.contrib.auth.models import User


# =========================
# Post Model
# =========================
class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"


# =========================
# Comment Model (Adjacency List)
# =========================
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Comment {self.id}"


# =========================
# Like Model (Explicit FKs)
# =========================
class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Prevent double-like on posts
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_like'
            ),
            # Prevent double-like on comments
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment_like'
            ),
        ]
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        target = self.post if self.post else self.comment
        return f"{self.user.username} liked {target}"
