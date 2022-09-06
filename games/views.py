from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAuthorOrReadOnly
from .models import GameReview
from .serializers import GameReviewSerializer
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from igdb.wrapper import IGDBWrapper
import requests
import json
import time


class GameReviewListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    queryset = GameReview.objects.all()
    serializer_class = GameReviewSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']  # dal più nuovo

    def perform_create(self, serializer):
        """CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DEL POST"""

        if self.request.user.id == int(self.request.data['author']):
            serializer.save()
        else:
            raise PermissionDenied(
                detail="Request Failed - Different User and Author")


class GameReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = GameReview.objects.all()
    serializer_class = GameReviewSerializer

    def perform_update(self, serializer):
        """CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DEL POST"""
        if self.request.user.id == int(self.request.data['author']):
            serializer.save()
        else:
            raise PermissionDenied(
                detail="Request Failed - Different User and Author")


class GameReviewByUserListView(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = GameReviewSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']  # dal più nuovo

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(), username=self.kwargs['username'])
        return GameReview.objects.filter(author=user)


class GameReviewByGameIdListView(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = GameReviewSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']  # dal più nuovo

    def get_queryset(self):
        return GameReview.objects.filter(gameId=self.kwargs['gameId'])


IGDB_AUTH_TOKEN = settings.IGDB_AUTH_TOKEN
IGDB_CLIENT_ID = settings.IGDB_CLIENT_ID

wrapper = IGDBWrapper(IGDB_CLIENT_ID, IGDB_AUTH_TOKEN)

def games_genres():
    '''RITORNA UN DIZIONARIO DEI GENERI OTTENUTI DA IGDB'''

    generi_byte = wrapper.api_request(
    'genres',
    'fields id,name; limit 50; sort id asc;'
    )
    generi = json.loads(generi_byte)

    diz_generi = {}
    for genere in generi:
        diz_generi[genere['name']] = genere['id']
    return diz_generi


class IGDBLatestGamesApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            now = str(int(time.time()))
            print(now)

            recentGames_byte = wrapper.api_request(
                'games',
                (f'fields id, name, first_release_date, rating, category, cover.image_id, genres.name, platforms.name;\
                    sort first_release_date desc;\
                    where first_release_date!=null & first_release_date<{now} & rating!=null & cover!=null;')
            )
            response = {}
            response['Recent'] = json.loads(recentGames_byte)

            if 'generi' in request.data.keys():
                    diz_generi = games_genres()
                    for genere in request.data['generi']:
                        if genere in diz_generi.keys():
                            giochi_per_genere = wrapper.api_request(
                                'games',
                                (f'fields id, name, first_release_date, rating, category, cover.image_id, genres.name;\
                                    sort first_release_date desc;\
                                    where genres=({diz_generi[genere]}) & first_release_date!=null & first_release_date<{now} & rating!=null & cover!=null;')
                            )
                            response[genere] = json.loads(giochi_per_genere)

            return Response(response, status=status.HTTP_200_OK)
            
        except requests.exceptions.HTTPError as e:
            return Response(f'Errore: {e}', status=status.HTTP_400_BAD_REQUEST)
        except BaseException as b:
            return Response(f'Errore: {b}', status=status.HTTP_400_BAD_REQUEST)


class IGDBSearchGamesApiView(APIView):
    '''API RITORNA IL GIOCO CERCATO TRAMITE POST'''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if 'query' in  request.data.keys():
            try:
                search_byte = wrapper.api_request(
                'games',
                f'search "{request.data["query"]}"; fields name, platforms, summary, storyline, cover.image_id, first_release_date,release_dates.date, release_dates.platform.name, rating;\
                limit 50; where rating != null;'
                )
                search_list = json.loads(search_byte)
                # search = tmdb.Search()
                # search.movie(query=request.data['query'], language='it')
                return Response(search_list, status=status.HTTP_200_OK)
            except requests.exceptions.HTTPError as e:
                return Response(f'Errore: {e}', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("{'error': 'query search not provided'}", status=status.HTTP_400_BAD_REQUEST)


class IGDBGameDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if 'gameID' in request.data.keys():
            try:
                id = request.data['gameID']
                gamebyID_byte = wrapper.api_request(
                    'games',
                    (f'fields id, name, first_release_date, summary, storyline, rating, category,\
                    cover.image_id, genres.name, platforms.name, release_dates.date, release_dates.platform.name, first_release_date,\
                    similar_games.name, similar_games.cover.image_id, involved_companies.company.name,\
                    involved_companies.developer, involved_companies.publisher, involved_companies.supporting, involved_companies.porting;\
                    where id={id};')
                )
                gamebyID_string = json.loads(gamebyID_byte)
                
                return Response(gamebyID_string, status=status.HTTP_200_OK)

            except requests.exceptions.HTTPError as e:
                return Response(f'Errore: {e}', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("{'error': 'gameID not provided'}", status=status.HTTP_400_BAD_REQUEST)
