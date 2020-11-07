from rest_framework import serializers

from takto_api.apps.business.models import Business, User, UserInRoom, Room


class BusinessSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(source='categories.name', child=serializers.CharField())

    class Meta:
        model = Business
        fields = ('business_id', 'name', 'state', 'city', 'address', 'postal_code', 'latitude', 'longitude', 'stars',
                  'review_count', 'is_open', 'attributes', 'hours', 'categories')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only_fields = ('device_id',)
        fields = ('username',)


class UserInRoomSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserInRoom
        fields = ('status', 'username')


class RoomSerializer(serializers.ModelSerializer):
    users = UserInRoomSerializer(source='user_in_room', read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('room_id', 'created_at', 'users')


class UserWithRoomsSerializer(UserSerializer):
    rooms = RoomSerializer(source='user_in_room.room')

    Meta = UserSerializer.Meta
