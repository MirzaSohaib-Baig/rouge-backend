from django.utils import timezone
from django_rest_authentication.exceptions import create_200_response, create_201_response, create_400_response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView

from .serializers import *


class StartLiveSession(CreateAPIView):

    serializer_class = StreamSessionSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        data['streamer'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return create_201_response(message="Live Session Started", data=serializer.data)
        return create_400_response(message=serializer.errors)

class EndLiveSession(UpdateAPIView):

    def update(self, request, *args, **kwargs):

        stream = StreamSession.objects.get(streamer=request.user)
        if stream.is_live:
            stream.is_live = False
            stream.ended_at = timezone.now()
            stream.save()
            return create_200_response(message="Stream ended successfully.")
        return create_400_response(message="Stream is already ended.")

class PublicLiveStreamersList(ListAPIView):

    queryset = StreamSession.objects.filter(is_live=True)
    serializer_class = StreamSessionSerializer

