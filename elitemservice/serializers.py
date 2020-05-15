from rest_framework import serializers

from elservicecollection.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    name_service = serializers.CharField()
    about_service = serializers.CharField()
    tags_service = serializers.ListField()

    class Meta:
        model = Service
        fields = '__all__'