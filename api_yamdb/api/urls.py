from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = '%(app_label)s'

v1_router = DefaultRouter()

v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
