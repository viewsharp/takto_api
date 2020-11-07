from rest_framework import serializers

from takto_api.apps.business.models import Business


class BusinessSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(source='categories.name', child=serializers.CharField())

    class Meta:
        model = Business
        fields = ('business_id', 'name', 'state', 'city', 'address', 'postal_code', 'latitude', 'longitude', 'stars',
                  'review_count', 'is_open', 'attributes', 'hours', 'categories')
