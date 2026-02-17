from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['provider', 'status', 'created_at']
