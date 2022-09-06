from rest_framework import serializers
# from .models import Profile

# class ProfileSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField() # chiama il methodo get_<field_name>
#     def get_username(self,obj):
#         return obj.user.username  # trova l'username

#     class Meta:
#         model = Profile
#         fields = ('id','username','image', 'user')
    

from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField() # chiama il methodo get_<field_name>
    # def get_username(self,obj):
    #     return obj.username  # trova l'username
    image = serializers.ImageField(allow_empty_file=True, allow_null=True, required=False) # consente la cencellazione dell'immagine
    class Meta:
        model = get_user_model()
        fields = ('id','username','image')
    