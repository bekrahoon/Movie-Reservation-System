import hashlib
import hmac
import time
from urllib.parse import parse_qs


def verify_init_data(init_data: str, bot_token: str, max_age: int = 86400) -> dict | None:
    """Проверка подписи Telegram initData по схеме HMAC-SHA256.

    Возвращает dict с данными при успехе, None при невалидной подписи или истёкшем auth_date.
    """
    parsed = parse_qs(init_data, keep_blank_values=True)
    if "hash" not in parsed:
        return None

    received_hash = parsed.pop("hash")[0]

    # Сортируем оставшиеся пары key=value по ключу
    data_check_pairs = []
    for key in sorted(parsed.keys()):
        data_check_pairs.append(f"{key}={parsed[key][0]}")
    data_check_string = "\n".join(data_check_pairs)

    # secret = HMAC_SHA256("WebAppData", bot_token)
    secret_key = hmac.new(
        b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256
    ).digest()

    # Вычисляем HMAC от data-check-string
    computed_hash = hmac.new(
        secret_key, data_check_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # Сравнение с защитой от timing-атак
    if not hmac.compare_digest(computed_hash, received_hash):
        return None

    # Проверка auth_date — отвергаем данные старше max_age секунд (по умолчанию 24 часа)
    auth_date_str = parsed.get("auth_date", [None])[0]
    if not auth_date_str:
        return None
    try:
        auth_date = int(auth_date_str)
    except (ValueError, TypeError):
        return None
    if time.time() - auth_date > max_age:
        return None

    # Собираем результат обратно в словарь (одно значение на ключ)
    result = {k: v[0] for k, v in parsed.items()}
    return result
