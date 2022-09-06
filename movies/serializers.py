from rest_framework import serializers
from .models import MovieReview

class MovieReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField() # chiama il methodo get_<field_name>
    def get_author_name(self,obj):
        return obj.author.username
    
    profile_image = serializers.SerializerMethodField()
    def get_profile_image(self, obj):
        url = obj.author.image.url
        request = self.context['request']
        return request.build_absolute_uri(url)

    class Meta:
        model = MovieReview
        fields = ('id','author','author_name', 'profile_image', 'title','movieId','review','rating','favourite','created_at', 'updated_at')
