from django.urls import path
from .views import (
    PostListAPIView,
    LikeAPIView,
    LeaderboardAPIView,
)

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('like/', LikeAPIView.as_view(), name='like'),
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
]
