from django.http import Http404
from rest_framework import pagination, generics, status, response, decorators

from takto_api.api.business.serializers import BusinessSerializer, UserSerializer, RoomSerializer
from takto_api.apps.business.models import Business, User, UserInRoom, Room


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20


class BusinessListAPIView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    pagination_class = DefaultPageNumberPagination
    queryset = Business


class BusinessRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer
    lookup_field = 'business_id'
    queryset = Business


@decorators.authentication_classes([])
class UserCreateRetrieveAPIView(generics.RetrieveAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(device_id=request.META['HTTP_AUTHORIZATION'])
        except User.DoesNotExist:
            user = None

        data = {**request.data, 'device_id': request.META['HTTP_AUTHORIZATION']}
        serializer = self.get_serializer(instance=user, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RoomCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        room = serializer.save()
        UserInRoom.objects.create(room=room, user=self.request.user)
        serializer.save()


class RoomRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    lookup_field = 'room_id'
    queryset = Room


class JoinToRoomAPIView(RoomRetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        room = self.get_object()
        UserInRoom.objects.create(room=room, user=request.user)

        room.refresh_from_db()
        serializer = self.get_serializer(room)
        return response.Response(serializer.data)
