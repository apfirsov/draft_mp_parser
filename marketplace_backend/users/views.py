from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from phone_verify.api import VerificationViewSet
from phone_verify.models import SMSVerification
from phone_verify import serializers as phone_serializers

from . import serializers
from .models import User

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from django_telegram_login.widgets.constants import (
    SMALL, 
    MEDIUM, 
    LARGE,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError, 
    TelegramDataIsOutdatedError,
)

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL

from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError, 
    TelegramDataIsOutdatedError,
)


def index(request):
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')
    try:
        result = verify_telegram_authentication(bot_token=bot_token, request_data=request.GET)
    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')
    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')
    return HttpResponse('Hello, ' + result['first_name'] + '!')


def get_auth_widget(request):
    telegram_login_widget = create_redirect_login_widget(
        redirect_url, bot_name, size=LARGE, user_photo=DISABLE_USER_PHOTO
    )
    context = {'telegram_login_widget': telegram_login_widget}
    return render(request, 'telegram_widget.html', context)


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
