from django.urls import include, path
from rest_framework.routers import SimpleRouter

from reviews.views import CommentViewSet, ReviewViewSet

review_v1_router = SimpleRouter()
review_v1_router.register('reviews', ReviewViewSet, basename='review')


comment_v1_router = SimpleRouter()
comment_v1_router.register('comments', CommentViewSet, basename='comment')


urlpatterns = [
    path(
        'v1/titles/<int:title_id>/reviews/<int:review_id>/',
        include(comment_v1_router.urls),
    ),
    path('v1/titles/<int:title_id>/', include(review_v1_router.urls)),
]
