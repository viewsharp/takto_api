from django.urls import path

from takto_api.api.business.views import (BusinessListAPIView, ChoiceAPIView,
                                          JoinToRoomAPIView, RoomCreateAPIView,
                                          RoomRetrieveAPIView,
                                          UserCreateRetrieveAPIView)

app_name = 'api'

urlpatterns = [
    path('v1/user', UserCreateRetrieveAPIView.as_view()),

    path('v1/room', RoomCreateAPIView.as_view()),
    path('v1/room/<str:room_id>', RoomRetrieveAPIView.as_view()),
    path('v1/room/<str:room_id>/join', JoinToRoomAPIView.as_view()),
    path('v1/room/<str:room_id>/choice', ChoiceAPIView.as_view()),
    path('v1/room/<str:room_id>/business', BusinessListAPIView.as_view()),
]
