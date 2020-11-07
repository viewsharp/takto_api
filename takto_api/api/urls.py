from django.urls import path

from takto_api.api.business.views import BusinessListAPIView, BusinessRetrieveAPIView

app_name = 'api'

urlpatterns = [
    path('v1/business', BusinessListAPIView.as_view()),
    path('v1/business/<str:business_id>', BusinessRetrieveAPIView.as_view())
]
