from django.contrib import admin
from .models import MovieReview 


# admin.site.register(MovieReview)

class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'movieId')
    list_filter = ('title', 'author','rating', 'movieId')
    search_fields = ('title',)

admin.site.register(MovieReview, MoviesAdmin)
