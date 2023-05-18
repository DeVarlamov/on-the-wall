from api.V1.filters import TitleFilter
from api.V1.permissions import (IsAdmin, IsAdminModeratorAuthorPermission,
                                IsAdminUserOrReadOnly)
from api.V1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, RegisterDataSerializer,
                                ReviewSerializer, TitleGetSerializer,
                                TitlePostSerializer, TokenSerializer,
                                UserEditSerializer, UserSerializer)
from api.V1.viewsets import CreateListDestroyViewSet
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from reviews.models import Category, Genre, Review, Title
from user.models import User


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Функция создание  для регистрации новых пользователей."""
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = serializer.save()
    except ValidationError as error:
        return Response(
            {'detail': str(error)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDb registration',
        message=f'Your confirmation code: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """Функция просмотра для генерации токена аутентификации JWT."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )

    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code'],
    ):
        token = tokens.AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(
        {'detail': 'неверный код'},
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset для обработки пользовательских операций CRUD.
    Предоставляет следующие конечные точки:
    - /users/ - GET and POST и публиковать
    для просмотра и создания пользователей
    - /users/me/ - ПОЛУЧИТЬ и исправить для просмотра и обновления профиля
    аутентифицированного пользователя
    """

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    filter_backends = (SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        request.method == 'PATCH'
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(CreateListDestroyViewSet):
    """
    Viewset для обработки операций CRUD по жанрам.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Viewset для обработки операций CRUD по категориям.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Viewset для обработки операций CRUD по тайтлам.
    """

    queryset = (
        Title.objects.select_related('category')
        .prefetch_related('genre')
        .annotate(rating=Avg('reviews__score'))
        .all()
        .order_by('name')
    )

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

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
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_comment(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)
        return review

    def get_queryset(self):
        return self.get_comment().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_comment())
