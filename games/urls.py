from django.urls import path
from .views import (GameReviewListView, GameReviewDetail, GameReviewByUserListView,
  GameReviewByGameIdListView, IGDBLatestGamesApiView, IGDBSearchGamesApiView, IGDBGameDetailAPIView)

urlpatterns = [
  path('', GameReviewListView.as_view(), name="GameReviewListView"),
  path('<int:pk>/', GameReviewDetail.as_view(), name="GameReviewDetail"),
  path('byuser/<username>/', GameReviewByUserListView.as_view(), name="GameReviewByUserListView"),
  path('bygameId/<int:gameId>/', GameReviewByGameIdListView.as_view(), name="GameReviewByGameIdListView"),
  path('igdb/games/', IGDBLatestGamesApiView.as_view(), name="IGDBLatestGamesApiView"),
  path('igdb/search/', IGDBSearchGamesApiView.as_view(), name="IGDBSearchGamesApiView"),
  path('igdb/gamebyID/', IGDBGameDetailAPIView.as_view(), name="IGDBGameDetailAPIView"),
]
