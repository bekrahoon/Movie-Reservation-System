import json

import phonenumbers
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from telegram_app.utils import verify_init_data
from user_register.models import Profile


def mini_app_page(request):
    return render(request, "telegram_app/mini_app.html")


def _get_telegram_user(validated_data: dict) -> tuple[int | None, str]:
    """Извлекает telegram_id и имя из провалидированных данных initData."""
    user_json = validated_data.get("user")
    if not user_json:
        return None, ""
    try:
        user_data = json.loads(user_json)
    except (json.JSONDecodeError, TypeError):
        return None, ""
    tg_id = user_data.get("id")
    first_name = user_data.get("first_name", "")
    return tg_id, first_name


def _login_user(request, user):
    """Логин через Django-сессию — тот же механизм, что и на сайте."""
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")


@csrf_exempt
@require_POST
def telegram_auth(request):
    """Первый шаг: проверка initData и попытка найти юзера по telegram_id."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Невалидный JSON"}, status=400)

    init_data = body.get("initData", "")
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return JsonResponse({"error": "Бот не настроен"}, status=500)

    # Проверка подписи Telegram — НИКОГДА не доверяем без этого
    validated = verify_init_data(init_data, bot_token)
    if validated is None:
        return JsonResponse({"error": "Невалидная подпись initData"}, status=403)

    tg_id, first_name = _get_telegram_user(validated)
    if not tg_id:
        return JsonResponse({"error": "Нет данных пользователя в initData"}, status=400)

    # Ищем юзера по telegram_id
    try:
        profile = Profile.objects.select_related("user").get(telegram_id=tg_id)
        _login_user(request, profile.user)
        return JsonResponse({"status": "ok", "username": profile.user.username})
    except Profile.DoesNotExist:
        # Юзер с таким telegram_id не найден — нужен телефон
        return JsonResponse({"status": "phone_required"})


@csrf_exempt
@require_POST
def telegram_link(request):
    """Второй шаг: привязка телефона + telegram_id, логин."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Невалидный JSON"}, status=400)

    init_data = body.get("initData", "")
    raw_phone = body.get("phone", "")
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return JsonResponse({"error": "Бот не настроен"}, status=500)

    # Повторная проверка подписи — каждый запрос валидируется заново
    validated = verify_init_data(init_data, bot_token)
    if validated is None:
        return JsonResponse({"error": "Невалидная подпись initData"}, status=403)

    tg_id, first_name = _get_telegram_user(validated)
    if not tg_id:
        return JsonResponse({"error": "Нет данных пользователя в initData"}, status=400)

    # Нормализация телефона в E.164
    try:
        parsed_phone = phonenumbers.parse(raw_phone, None)
    except phonenumbers.NumberParseException:
        return JsonResponse({"error": "Некорректный номер телефона"}, status=400)
    if not phonenumbers.is_valid_number(parsed_phone):
        return JsonResponse({"error": "Номер телефона невалиден"}, status=400)
    phone_e164 = phonenumbers.format_number(
        parsed_phone, phonenumbers.PhoneNumberFormat.E164
    )

    # Ищем существующий аккаунт по phone
    try:
        profile = Profile.objects.select_related("user").get(phone=phone_e164)
    except Profile.DoesNotExist:
        profile = None

    if profile:
        # Коллизия: номер уже привязан к аккаунту с ДРУГИМ telegram_id
        if profile.telegram_id is not None and profile.telegram_id != tg_id:
            return JsonResponse(
                {"error": "Этот номер уже привязан к другому Telegram-аккаунту"},
                status=409,
            )
        # Привязываем telegram_id к найденному аккаунту (НЕ создаём второй)
        profile.telegram_id = tg_id
        profile.save()
        _login_user(request, profile.user)
        return JsonResponse({"status": "ok", "username": profile.user.username})

    # Аккаунта с таким номером нет — создаём нового юзера
    username = f"tg_{tg_id}"
    if User.objects.filter(username=username).exists():
        username = f"tg_{tg_id}_{int(__import__('time').time())}"
    user = User.objects.create_user(username=username, first_name=first_name or "")
    user.set_unusable_password()
    user.save()
    # Профиль создастся через сигнал post_save, но нужно обновить поля
    profile = user.profile
    profile.phone = phone_e164
    profile.telegram_id = tg_id
    profile.save()
    _login_user(request, user)
    return JsonResponse({"status": "ok", "username": user.username, "created": True})
