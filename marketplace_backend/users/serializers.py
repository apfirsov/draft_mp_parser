from rest_framework import serializers

from .models import User, Status


class CustomUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_status(self, obj):
        if self.context.get('request').user.is_anonymous:
            return Status.objects.get(status='Unregistered')
        return Status.objects.get(status='Registered')
