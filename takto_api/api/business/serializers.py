from rest_framework import serializers

from takto_api.apps.business.models import Business, User, UserInRoom, Room, Photo, Choice, Category


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo_id', 'caption', 'label')


class CategorySerializer(serializers.Serializer):
    def to_representation(self, instance: Category):
        return instance.name


class BusinessSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Business
        fields = ('business_id', 'name', 'state', 'city', 'address', 'postal_code', 'latitude', 'longitude', 'stars',
                  'review_count', 'is_open', 'attributes', 'hours', 'categories', 'photos')


class UserSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'device_id')


class UserInRoomSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    ready = serializers.BooleanField()

    class Meta:
        model = UserInRoom
        fields = ('username', 'ready')


class RoomSerializer(serializers.ModelSerializer):
    users = UserInRoomSerializer(source='user_in_room', read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('room_id', 'created_at', 'users')


class UserWithRoomsSerializer(UserSerializer):
    rooms = RoomSerializer(source='user_in_room.room')

    Meta = UserSerializer.Meta


class ChoiceSerializer(serializers.ModelSerializer):
    first_business = BusinessSerializer(read_only=True)
    second_business = BusinessSerializer(read_only=True)

    class Meta:
        model = Choice
        fields = ('first_business', 'second_business', 'first_business_chosen')
