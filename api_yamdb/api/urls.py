from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    register,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
