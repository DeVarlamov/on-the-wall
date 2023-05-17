from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.V1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    register,
)

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', register, name='register'),
    path('token/', get_jwt_token, name='token'),
]
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_urls)),
]
