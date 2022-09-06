from rest_framework import generics
# from .models import Profile
# from .serializers import ProfileSerializer
from .permission import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

from drf_multiple_model.views import ObjectMultipleModelAPIView
from django.shortcuts import get_object_or_404
import movies

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer    

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'username'
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

# drf_multiple_model
class UserListDetail(ObjectMultipleModelAPIView):
    def get_querylist(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        querylist = [
            {
                'queryset': get_user_model().objects.filter(username=self.kwargs['username']),
                'serializer_class': UserSerializer,
                'permission_classes': (IsAuthorOrReadOnly,),
                'lookup_field':'username',
            },
            {
                'serializer_class': movies.serializers.MovieReviewSerializer,
                'queryset': movies.models.MovieReview.objects.filter(author=user),

            },
        ]
        return querylist
    

class GetUserFromToken(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            access_token_obj = AccessToken(request.data['token'])
            user_id = access_token_obj['user_id']
            user = get_user_model().objects.get(id=user_id)
            content =  {'user_id': user_id, 'user':user.username, 'email':user.email}
            return Response(content, status=status.HTTP_200_OK)

        except KeyError:
            # print("key error")
            return Response({"Key Error": "Token key must given"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as err:
            # print("Token Error")
            # print(err)
            return Response({"Token Error": str(err)}, status=status.HTTP_400_BAD_REQUEST) 
        except BaseException as err:
            # print("ERRORE")
            # print(type(err))
            return Response({"Error": "Error"}, status=status.HTTP_400_BAD_REQUEST)


#####################################################################################





# class UserList(generics.ListAPIView):
#     permission_classes = (IsAuthorOrReadOnly,)
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer    

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'user'
#     permission_classes = (IsAuthorOrReadOnly,)
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


    
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'username'
#     permission_classes = (IsAuthorOrReadOnly,)
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
    


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'username'
#     permission_classes = (IsAuthorOrReadOnly,)


# from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet

# class UserReviewsList(ObjectMultipleModelAPIViewSet):
#     querylist = [
#         {'queryset': get_user_model().objects.all(), 'serializer_class': UserSerializer, 'lookup_field':'username'},
#         {'queryset': movies.models.MovieReview.objects.all(), 'serializer_class': movies.serializers.MovieReviewSerializer}
#     ]


# class UserList(ObjectMultipleModelAPIView):
#     querylist = [
#         {'queryset': get_user_model().objects.all(), 'serializer_class': UserSerializer, 'permission_classes': (IsAuthorOrReadOnly,)},
#         {'queryset': movies.models.MovieReview.objects.all(), 'serializer_class': movies.serializers.MovieReviewSerializer}
#     ]