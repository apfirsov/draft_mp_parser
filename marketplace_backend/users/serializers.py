from rest_framework import serializers

from phone_verify.serializers import SMSVerificationSerializer

from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def get_status(self, obj):
        return 'Registered'


class CustomUserSMSSerializer(CustomUserSerializer, SMSVerificationSerializer):
    pass
