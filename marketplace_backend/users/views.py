from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from phone_verify.api import VerificationViewSet
from phone_verify.models import SMSVerification
from phone_verify import serializers as phone_serializers

from . import serializers
from .models import User


class CustomUserViewSet(VerificationViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_and_register(self, request):
        serializer = phone_serializers.SMSVerificationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer = serializers.CustomUserSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = User(**serializer.validated_data)
        user.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        serializer = phone_serializers.SMSVerificationSerializer(
            data=request.data
        )
        phone_number = serializer.initial_data['phone_number']
        SMSVerification.objects.get(phone_number=phone_number).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
