from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAuthorOrReadOnly
from .models import AlbumReview
from .serializers import AlbumReviewSerializer
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from rest_framework.response import Response
import requests



class AlbumReviewListView(generics.ListCreateAPIView):
	permission_classes = (IsAuthorOrReadOnly,
						  permissions.IsAuthenticatedOrReadOnly)
	queryset = AlbumReview.objects.all()
	serializer_class = AlbumReviewSerializer
	filter_backends = [OrderingFilter]
	ordering = ['-created_at']  # dal più nuovo

	def perform_create(self, serializer):
		"""CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DEL POST"""

		if self.request.user.id == int(self.request.data['author']):
			serializer.save()
		else:
			raise PermissionDenied(
				detail="Request Failed - Different User and Author")


class AlbumReviewDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthorOrReadOnly,)
	queryset = AlbumReview.objects.all()
	serializer_class = AlbumReviewSerializer

	def perform_update(self, serializer):
		"""CONTROLLA SE L'USER LOGGATO SIA UGUALE A L'AUTORE DEL POST"""
		if self.request.user.id == int(self.request.data['author']):
			serializer.save()
		else:
			raise PermissionDenied(
				detail="Request Failed - Different User and Author")


class AlbumReviewByUserListView(generics.ListAPIView):
	permission_classes = (IsAuthorOrReadOnly,)
	serializer_class = AlbumReviewSerializer
	filter_backends = [OrderingFilter]
	ordering = ['-created_at']  # dal più nuovo

	def get_queryset(self):
		user = get_object_or_404(
			get_user_model(), username=self.kwargs['username'])
		return AlbumReview.objects.filter(author=user)


class AlbumReviewByAlbumIdListView(generics.ListAPIView):
	permission_classes = (IsAuthorOrReadOnly,)
	serializer_class = AlbumReviewSerializer
	filter_backends = [OrderingFilter]
	ordering = ['-created_at']  # dal più nuovo

	def get_queryset(self):
		return AlbumReview.objects.filter(albumId=self.kwargs['albumId'])


auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager, language='IT')


def music_genres():
  genres = sp.recommendation_genre_seeds()
  return genres['genres']


class SpotifyLatestAlbumsApiView(APIView):
	'''API CHE RITORNA UNA LISTA DI ALBUM USCITI DI RECENTE
	   E UNA LISTA DI ALBUM PER OGNI GENERE'''
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		response = {}
		new_release = sp.new_releases(country='IT', limit=20)
		response['new_release'] = new_release['albums']['items']

		try:
			if 'generi' in request.data.keys():
				lista_generi = music_genres()
				for genere in request.data['generi']:
					if genere in lista_generi:
						recommendations = sp.recommendations(seed_genres=[genere], limit=15, country='IT')
						if 'tracks' in recommendations.keys():
							response[genere] = []
							for track in recommendations['tracks']:
								if 'album' in track.keys():
									# if track['album']['album_type'].upper() != 'SINGLE':
									response[genere].append(track['album'])

			return Response(response, status=status.HTTP_200_OK)
		except spotipy.client.SpotifyException as e:
			return Response(f"{'error': {e} }", status=status.HTTP_400_BAD_REQUEST)


class SpotifyAlbumDetailAPIView(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		if 'albumID' in request.data.keys():
			try:
				album = sp.album(album_id=request.data['albumID'])
				next_tracks = album['tracks']

				# ciclo while per aggiungere tutte le tracce dell'album (album['tracks']['items'])
				# se le tracce nell'album sono più del limite di richiesta impostato da spotify(50), album['tracks']['next'] contiene url per le prossime 50 tracce, e così via
				while next_tracks['next'] is not None:
					next_tracks = sp.next(next_tracks)
					album['tracks']['items'].extend(next_tracks['items'])
				
				album_id = album['id']
				artists = album['artists'] 

				recommendations = sp.recommendations(seed_artists=[artist['id'] for artist in artists], country='IT')
				
				similar_album = []
				for track in recommendations['tracks']:
					if (track['album']['id'] != album_id) and (track['album'] not in similar_album):
						similar_album.append(track['album'])

				album['similar'] = similar_album
					
				# print(album)
				return Response(album, status=status.HTTP_200_OK)

			except spotipy.client.SpotifyException:
				return Response("{'error': '400  invalid ID' }", status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response("{'error': 'albumID not provided'}", status=status.HTTP_400_BAD_REQUEST)


# album_search =  sp.search(q='album:Drones', type='album')
# albums_items = album_search['albums']['items']

class SpotifySearchAlbumsApiView(APIView):
	'''CERCA ALBUM'''
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		if 'query' and 'type' in request.data.keys():
			try:
				# ES. album_search =  sp.search(q='album:Drones', type='album')
				album_search =  sp.search(q=f"{request.data['type']}:{request.data['query']}", type='album', limit=50)
				return Response(album_search['albums']['items'], status=status.HTTP_200_OK)

			except spotipy.client.SpotifyException as err:
				return Response(f"{'error': '{err}' }", status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response("{'error': 'query or type not provided'}", status=status.HTTP_400_BAD_REQUEST)
