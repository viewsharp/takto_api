from rest_framework import decorators, generics, pagination, response, status

from takto_api.api.business.serializers import (BusinessSerializer,
                                                ChoiceSerializer,
                                                RoomSerializer, UserSerializer)
from takto_api.apps.business.models import (Business, Choice, Room, User,
                                            UserInRoom)


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20


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
        serializer = self.get_serializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RoomCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        room = serializer.save()
        UserInRoom.create_object_with_choice(room=room, user=self.request.user)
        serializer.save()


class RoomRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    lookup_field = 'room_id'
    queryset = Room.objects.all()


class JoinToRoomAPIView(RoomRetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        room = self.get_object()
        UserInRoom.create_object_with_choice(room=room, user=request.user)

        room.refresh_from_db()
        serializer = self.get_serializer(room)
        return response.Response(serializer.data)


class ChoiceAPIView(generics.GenericAPIView):
    serializer_class = ChoiceSerializer

    def put(self, request, *args, **kwargs):
        user_in_room = self.get_user_in_room()
        
        prev_choice = self.get_object(user_in_room=user_in_room)
        serializer = self.get_serializer(prev_choice, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if user_in_room.ready:
            return response.Response()

        new_choice = Choice.create_random_object(
            user_in_room=prev_choice.user_in_room,
            first_business=prev_choice.first_business if prev_choice.first_business_chosen else prev_choice.second_business
        )
        serializer = self.get_serializer(new_choice)
        return response.Response(serializer.data)
    
    def get(self, request, *args, **kwargs):
        user_in_room = self.get_user_in_room()

        if user_in_room.ready:
            return response.Response()
        
        instance = self.get_object(user_in_room)
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    def get_object(self, user_in_room=None):
        user_in_room = user_in_room or self.get_user_in_room()
        
        return Choice.objects.get(user_in_room=user_in_room, first_business_chosen__isnull=True)
    
    def get_user_in_room(self):
        return UserInRoom.objects.get(room__room_id=self.kwargs['room_id'], user=self.request.user)


class BusinessListAPIView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    pagination_class = DefaultPageNumberPagination
    queryset = Business.objects.filter(photos__isnull=False)
