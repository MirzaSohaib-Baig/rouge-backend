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

    def create(self, request, *args, **kwargs):

        post_data = {

        }

        post_serializer = PostSerializer(data=post_data)
        if not post_serializer.is_valid():
            create_400_response(message="Invalid Data")
        post_serializer.save()
        return create_201_response(message="Post Created")