from rest_framework import serializers
from .models import GameReview

class GameReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField() # chiama il methodo get_<field_name>
    def get_author_name(self,obj):
        return obj.author.username  # sostituisce id author con l'username
    
    profile_image = serializers.SerializerMethodField()
        try:
            url = obj.author.image.url
            request = self.context['request']
            return request.build_absolute_uri(url)
        except ValueError:
            return None
    
    class Meta:
        model = GameReview
        fields = ('id','author','author_name','profile_image', 'title','gameId','review','rating','favourite','created_at', 'updated_at')
