from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from django_rest_authentication.exceptions import *
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *
from django_rest_authentication.exceptions import create_400_response, create_201_response


class CreatePostUser(CreateAPIView):

    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        # Convert to mutable QueryDict
        data = request.data.copy()
        data['author'] = request.user.id

        # Re-assign list fields properly
        if 'mentions' in request.data:
            data.setlist('mentions', request.data.getlist('mentions'))

        if 'tags' in request.data:
            data.setlist('tags', request.data.getlist('tags'))

        if 'media' in request.FILES:
            data.setlist('media', request.FILES.getlist('media'))

        post_serializer = PostSerializer(data=data)

        if not post_serializer.is_valid():
            return create_400_response(message="Invalid Data", data=post_serializer.errors)

        post_serializer.save()
        return create_201_response(message="Post Created", data=post_serializer.data)


class PostListView(ListAPIView):
    
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        author_id = self.request.query_params.get('author')
        if author_id:
            return Post.objects.filter(author=author_id)
        return Post.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if serializer:
            return create_201_response(message="Posts Retrieved", data=serializer.data)
        return create_400_response(message=list(serializer.errors.values())[0][0])