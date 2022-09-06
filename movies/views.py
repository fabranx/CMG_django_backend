from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from .models import MovieReview
from .serializers import MovieReviewSerializer
from .permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
import tmdbsimple as tmdb
from django.conf import settings


class MovieReviewListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer  
    filter_backends = [OrderingFilter]
    ordering = ['-created_at'] # dal più nuovo
    # filter_fields = ['movieId']
    # ordering_fields = ['movieId'] 
    def perform_create(self, serializer):
        """CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DEL POST"""

        if self.request.user.id == int(self.request.data['author']):
            serializer.save()
        else:
            raise PermissionDenied(detail="Request Failed - Different User and Author")
      

class MovieReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer   

    def perform_update(self, serializer):
        """CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DEL POST"""
        if self.request.user.id == int(self.request.data['author']):
            serializer.save()
        else:
            raise PermissionDenied(detail="Request Failed - Different User and Author")



class MovieReviewByUserListView(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    # queryset = MovieReview.objects.filter()
    serializer_class = MovieReviewSerializer 
    filter_backends = [OrderingFilter]
    ordering = ['-created_at'] # dal più nuovo
    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return MovieReview.objects.filter(author=user)
      

class MovieReviewByMovieIdListView(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = MovieReviewSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-created_at'] # dal più nuovo
    def get_queryset(self):
        return MovieReview.objects.filter(movieId=self.kwargs['movieId'])




tmdb.API_KEY = settings.TMDB_API_KEY


def movie_genres_list():
    '''RITORNA UN DIZIONARIO DEI GENERI OTTENUTI DA TMDB'''
    genere = tmdb.Genres()
    res = genere.movie_list(language='it')
    diz_generi = {}
    for genere in res['genres']:
        diz_generi[genere['name']] = genere['id']
    return diz_generi


class TMDBLatestMoviesApiView(APIView):
    '''API RITORNA UNA LISTA DI FILM ORA AL CINEMA 
       E UNA LISTA DI FILM PER OGNI GENERE'''
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        movies = tmdb.Movies()
        # self.movies_response = movies.now_playing(language='it')
        # print('GENERI:', request.data)
        response = {}
        response['Film al Cinema'] = movies.now_playing(language='it')
        response['Popolari'] = movies.popular(language='it')
        response['In Arrivo'] = movies.upcoming(language='it')

        if 'generi' in request.data.keys():
            diz_generi = movie_genres_list()
            for genere in request.data['generi']:
                if genere in diz_generi.keys():
                    generi = tmdb.Genres(id=diz_generi[genere])
                    response[genere] = generi.movies(language='it', include_adult=False)
            

        return Response(response, status=status.HTTP_200_OK)


class TMDBSearchMoviesApiView(APIView):
    '''API RITORNA IL FILM CERCATO TRAMITE POST'''
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        if 'query' in request.data.keys():
            search = tmdb.Search()
            search.movie(query=request.data['query'], language='it')
            return Response(search.results, status=status.HTTP_200_OK)
        else:
            return Response("{'error': 'query search not provided'}", status=status.HTTP_400_BAD_REQUEST)


class TMDBMovieDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        import requests
        if 'movieID' in request.data.keys():
            try:
                movie = tmdb.Movies(id=request.data['movieID'])
                info = movie.info(language='it', append_to_response='credits,recommendations')
                return Response(info, status=status.HTTP_200_OK)

            except requests.exceptions.HTTPError:
                return Response("{'error': '404 not found' }", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("{'error': 'movieID not provided'}", status=status.HTTP_400_BAD_REQUEST)
