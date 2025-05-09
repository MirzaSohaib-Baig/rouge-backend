from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_rest_authentication.exceptions import *
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from django_rest_authentication.exceptions import create_400_response, create_201_response


class CreatePostUser(CreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):

        post_data = {
            "author": request.user.id,
            "group": request.data.get("group"),
            "content": request.data.get("content"),
            "visibility": request.data.get("visibility"),
            "is_paid": request.data.get("is_paid"),
            "price": request.data.get("price"),
            "media": request.FILES.getlist("media"),
            "mentions": request.data.get("mentions"),
            "tags": request.data.get("tags"),
            "payments": request.data.get("payments"),
        }

        post_serializer = PostSerializer(data=post_data)
        if not post_serializer.is_valid():
            create_400_response(message="Invalid Data")
        post_serializer.save()
        return create_201_response(message="Post Created")
    
    # def create(self, request, *args, **kwargs):
    #     post_data = {
    #         "author": request.user.id,
    #         "group": request.data.get("group"),
    #         "content": request.data.get("content"),
    #         "visibility": request.data.get("visibility"),
    #         "is_paid": request.data.get("is_paid"),
    #         "price": request.data.get("price"),
    #         "media": request.FILES.getlist("media"),
    #         "mentions": request.data.get("mentions"),
    #         "tags": request.data.get("tags"),
    #         "payments": request.data.get("payments"),
    #     }

    #     serializer = self.get_serializer(data=post_data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=201)

class PostListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user, is_active=True).order_by("-created_at")