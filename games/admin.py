from django.contrib import admin
from .models import GameReview 


class GamesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'gameId')
    list_filter = ('title', 'author','rating', 'gameId')
    search_fields = ('title',)

admin.site.register(GameReview, GamesAdmin)
