from posixpath import basename
from django.urls import path
from .views import UserListDetail, UserList, GetUserFromToken, UserDetail

urlpatterns = [
    path('userfromtoken/', GetUserFromToken.as_view(), name='GetUserFromToken'),
    path('user-reviews/<username>/', UserListDetail.as_view(), name='UserListDetail'),
    path('', UserList.as_view(), name='UserList'),
    path('<username>/', UserDetail.as_view(), name='UserListDetail'),
]


# from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register('users', UserViewSet, basename='users')
# # router.register('prova', UserReviewsList, basename='prova')

# urlpatterns += router.urls
