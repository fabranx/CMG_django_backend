from django.contrib import admin
from .models import AlbumReview 



class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'albumId')
    list_filter = ('title', 'author','rating', 'albumId')
    search_fields = ('title',)

admin.site.register(AlbumReview, MusicAdmin)
