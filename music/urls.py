from django.urls import path
from .views import (AlbumReviewListView, AlbumReviewDetail, AlbumReviewByUserListView,
  AlbumReviewByAlbumIdListView, SpotifyLatestAlbumsApiView, SpotifyAlbumDetailAPIView, SpotifySearchAlbumsApiView)

urlpatterns = [
  path('', AlbumReviewListView.as_view(), name="AlbumReviewListView"),
  path('<int:pk>/', AlbumReviewDetail.as_view(), name="AlbumReviewDetail"),
  path('byuser/<username>/', AlbumReviewByUserListView.as_view(), name="AlbumReviewByUserListView"),
  path('byAlbumId/<str:albumId>/', AlbumReviewByAlbumIdListView.as_view(), name="AlbumReviewByAlbumIdListView"),
  path('spotify/album/', SpotifyLatestAlbumsApiView.as_view(), name="SpotifyLatestAlbumsApiView"),
  path('spotify/search/', SpotifySearchAlbumsApiView.as_view(), name="SpotifySearchAlbumsApiView"),
  path('spotify/albumbyID/', SpotifyAlbumDetailAPIView.as_view(), name="SpotifyAlbumDetailAPIView"),
]
