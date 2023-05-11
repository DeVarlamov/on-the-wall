from django.urls import include, path
from rest_framework.routers import SimpleRouter

from reviews.views import ReviewViewSet

review_v1_router = SimpleRouter()
review_v1_router.register('reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('v1/titles/<int:title_id>/', include(review_v1_router.urls)),
]
