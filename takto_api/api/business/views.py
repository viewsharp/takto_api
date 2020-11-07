from rest_framework import pagination, generics

from takto_api.api.business.serializers import BusinessSerializer
from takto_api.apps.business.models import Business


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    page_size = 20


class BusinessListAPIView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        return Business.objects.all()


class BusinessRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = BusinessSerializer
    lookup_field = 'business_id'

    def get_queryset(self):
        return Business.objects.all()
