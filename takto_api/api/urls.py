from django.urls import path

from takto_api.api.business.views import BusinessListAPIView, BusinessRetrieveAPIView, UserCreateRetrieveAPIView, \
    RoomCreateAPIView, RoomRetrieveAPIView, JoinToRoomAPIView

app_name = 'api'

urlpatterns = [
    path('v1/business', BusinessListAPIView.as_view()),
    path('v1/business/<str:business_id>', BusinessRetrieveAPIView.as_view()),

    path('v1/user', UserCreateRetrieveAPIView.as_view()),

    path('v1/room', RoomCreateAPIView.as_view()),
    path('v1/room/<str:room_id>', RoomRetrieveAPIView.as_view()),
    path('v1/room/<str:room_id>/join', JoinToRoomAPIView.as_view()),
]
