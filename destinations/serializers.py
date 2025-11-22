from rest_framework import serializers
from .models import Destination, DestinationImage

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'caption', 'created_at']

class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Destination
        fields = ['id', 'place_name', 'slug', 'weather', 'state', 'district', 
                 'google_map_link', 'description', 'images', 'created_at', 'updated_at']