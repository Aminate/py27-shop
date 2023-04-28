from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Rating, Favorite
from .serializers import CommentSerializer, RatingSerializer, FavoriteSerializer
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAuthor


class CommentViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class FavoriteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AddRatingAPIView(APIView):
    @swagger_auto_schema(request_body=RatingSerializer())
    def post(self, request):
        ser = RatingSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=201)





