from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    register, CommentViewSet, ReviewViewSet,
)



v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')

review_v1_router = DefaultRouter()
review_v1_router.register('reviews', ReviewViewSet, basename='review')

comment_v1_router = DefaultRouter()
comment_v1_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', register, name='register'),
    path('auth/token/', get_jwt_token, name='token'),
    path('titles/<int:title_id>/', include(review_v1_router.urls)),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/',
        include(comment_v1_router.urls),
    ),
]
