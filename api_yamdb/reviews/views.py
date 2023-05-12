from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Review
from reviews.serilizers import ReviewSerializer, CommentSerializer

from api.permissions import IsAdminModeratorAuthorPermission

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()


    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    def get_comment(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_comment().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_comment())
