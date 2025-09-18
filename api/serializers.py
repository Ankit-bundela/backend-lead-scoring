
from rest_framework import serializers
from .models import Offer, Lead, LeadScore

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class LeadScoreSerializer(serializers.ModelSerializer):
    lead = LeadSerializer()
    offer = OfferSerializer()
    class Meta:
        model = LeadScore
        fields = '__all__'
