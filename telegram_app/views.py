import json

import phonenumbers
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from telegram_app.utils import verify_init_data
from user_register.models import Profile


def mini_app_page(request):
    return render(request, "telegram_app/mini_app.html")


def _login_user(request, user):
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")


@csrf_exempt
@require_POST
def telegram_auth(request):
    """Авто-аутентификация по номеру телефона.
    Получает initData + phone, проверяет подпись, ищет юзера по номеру.
    Найден → логин. Не найден → not_found (фронт отправит на /register/).
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Невалидный JSON"}, status=400)

    init_data = body.get("initData", "")
    raw_phone = body.get("phone", "")
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return JsonResponse({"error": "Бот не настроен"}, status=500)

    # Проверка подписи Telegram
    validated = verify_init_data(init_data, bot_token)
    if validated is None:
        return JsonResponse({"error": "Невалидная подпись initData"}, status=403)

    # Нормализация телефона в E.164
    try:
        parsed_phone = phonenumbers.parse(raw_phone, None)
    except phonenumbers.NumberParseException:
        return JsonResponse({"status": "not_found"})
    if not phonenumbers.is_valid_number(parsed_phone):
        return JsonResponse({"status": "not_found"})
    phone_e164 = phonenumbers.format_number(
        parsed_phone, phonenumbers.PhoneNumberFormat.E164
    )

    # Ищем юзера по номеру телефона
    try:
        profile = Profile.objects.select_related("user").get(phone=phone_e164)
        _login_user(request, profile.user)
        return JsonResponse({"status": "ok", "username": profile.user.username})
    except Profile.DoesNotExist:
        # Номер не зарегистрирован — пусть регистрируется как обычный юзер
        return JsonResponse({"status": "not_found"})


@csrf_exempt
@require_POST
def telegram_link(request):
    """Запасной эндпоинт для привязки телефона (используется из профиля на сайте)."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Невалидный JSON"}, status=400)

    init_data = body.get("initData", "")
    raw_phone = body.get("phone", "")
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return JsonResponse({"error": "Бот не настроен"}, status=500)

    validated = verify_init_data(init_data, bot_token)
    if validated is None:
        return JsonResponse({"error": "Невалидная подпись initData"}, status=403)

    try:
        parsed_phone = phonenumbers.parse(raw_phone, None)
    except phonenumbers.NumberParseException:
        return JsonResponse({"error": "Некорректный номер телефона"}, status=400)
    if not phonenumbers.is_valid_number(parsed_phone):
        return JsonResponse({"error": "Номер телефона невалиден"}, status=400)
    phone_e164 = phonenumbers.format_number(
        parsed_phone, phonenumbers.PhoneNumberFormat.E164
    )

    try:
        profile = Profile.objects.select_related("user").get(phone=phone_e164)
        _login_user(request, profile.user)
        return JsonResponse({"status": "ok", "username": profile.user.username})
    except Profile.DoesNotExist:
        return JsonResponse({"status": "not_found"})
