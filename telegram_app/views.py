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


def _get_telegram_user(validated_data: dict) -> tuple[int | None, str]:
    user_json = validated_data.get("user")
    if not user_json:
        return None, ""
    try:
        user_data = json.loads(user_json)
    except (json.JSONDecodeError, TypeError):
        return None, ""
    return user_data.get("id"), user_data.get("first_name", "")


def _login_user(request, user):
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")


@csrf_exempt
@require_POST
def telegram_auth(request):
    """Быстрый вход по telegram_id (без запроса контакта).
    Работает со второго раза — после того как telegram_id сохранён."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Невалидный JSON"}, status=400)

    init_data = body.get("initData", "")
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return JsonResponse({"error": "Бот не настроен"}, status=500)

    validated = verify_init_data(init_data, bot_token)
    if validated is None:
        return JsonResponse({"error": "Невалидная подпись initData"}, status=403)

    tg_id, _ = _get_telegram_user(validated)
    if not tg_id:
        return JsonResponse({"status": "phone_required"})

    # Ищем по telegram_id — мгновенный вход если уже привязан
    try:
        profile = Profile.objects.select_related("user").get(telegram_id=tg_id)
        _login_user(request, profile.user)
        return JsonResponse({"status": "ok", "username": profile.user.username})
    except Profile.DoesNotExist:
        return JsonResponse({"status": "phone_required"})


@csrf_exempt
@require_POST
def telegram_link(request):
    """Первый вход: ищет юзера по номеру телефона и сохраняет telegram_id.
    После этого все следующие входы будут мгновенными через telegram_auth."""
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

    tg_id, _ = _get_telegram_user(validated)
    if not tg_id:
        return JsonResponse({"error": "Нет данных пользователя"}, status=400)

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

    # Ищем юзера по номеру
    try:
        profile = Profile.objects.select_related("user").get(phone=phone_e164)
    except Profile.DoesNotExist:
        # Номер не зарегистрирован — пусть регистрируется на сайте
        return JsonResponse({"status": "not_found"})

    # Сохраняем telegram_id — в следующий раз вход будет мгновенным
    if profile.telegram_id is None:
        profile.telegram_id = tg_id
        profile.save()

    _login_user(request, profile.user)
    return JsonResponse({"status": "ok", "username": profile.user.username})
