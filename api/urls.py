from django.urls import path, include

urlpatterns = [
    path('movies/', include('movies.urls')),
    path('games/', include('games.urls')),
    path('music/', include('music.urls')),
    path('users/', include('users.urls')),
]
