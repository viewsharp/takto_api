from rest_framework import pagination, generics, status, response, decorators

from takto_api.api.business.serializers import BusinessSerializer, UserSerializer, RoomSerializer, ChoiceSerializer
from takto_api.apps.business.models import Business, User, UserInRoom, Room, Choice


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20


class BusinessListAPIView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    pagination_class = DefaultPageNumberPagination
    queryset = Business.objects.all()


class BusinessRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer
    lookup_field = 'business_id'
    queryset = Business.objects.all()


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
        UserInRoom.create_with_choice(room=room, user=self.request.user)
        serializer.save()


class RoomRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    lookup_field = 'room_id'
    queryset = Room.objects.all()


class JoinToRoomAPIView(RoomRetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        room = self.get_object()
        UserInRoom.create_with_choice(room=room, user=request.user)

        room.refresh_from_db()
        serializer = self.get_serializer(room)
        return response.Response(serializer.data)


class ChoiceRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ChoiceSerializer

    def put(self, request, *args, **kwargs):
        prev_choice = self.get_object()
        serializer = self.get_serializer(instance=prev_choice, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_choice = Choice.create_random(
            user_in_room=prev_choice.user_in_room,
            first_business=prev_choice.first_business if prev_choice.first_business_chosen else prev_choice.second_business
        )
        serializer = self.get_serializer(instance=new_choice)
        return response.Response(serializer.data)

    def get_object(self):
        return Choice.objects.get(
            user_in_room__room__room_id=self.kwargs['room_id'],
            user_in_room__user=self.request.user,
            first_business_chosen__isnull=True
        )
