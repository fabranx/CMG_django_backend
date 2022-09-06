from django.urls import path
from .views import  (
     MovieReviewListView, MovieReviewDetail, MovieReviewByUserListView, MovieReviewByMovieIdListView,
     TMDBLatestMoviesApiView, TMDBSearchMoviesApiView, TMDBMovieDetailAPIView)



urlpatterns = [
    path('', MovieReviewListView.as_view(), name="MovieReviewListView"),
    path('<int:pk>/', MovieReviewDetail.as_view(), name="MovieReviewDetail"),
    # path('byuser/<int:pk>/', MovieReviewByUserListView.as_view(), name="MovieReviewByUserListView"),
    path('byuser/<username>/', MovieReviewByUserListView.as_view(), name="MovieReviewByUserListView"),
    path('bymovieId/<int:movieId>/', MovieReviewByMovieIdListView.as_view(), name="MovieReviewByUserListView"),
    path('tmdb/movies/', TMDBLatestMoviesApiView.as_view(), name="TMDBLatestMoviesApiView"),
    path('tmdb/search/', TMDBSearchMoviesApiView.as_view(), name="TMDBSearchMoviesApiView"),
    path('tmdb/moviebyID/', TMDBMovieDetailAPIView.as_view(), name="TMDBMovieDetailAPIView"),

]
