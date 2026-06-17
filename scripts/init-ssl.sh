#!/bin/bash
# Получение SSL-сертификата Let's Encrypt
# Использование: ./scripts/init-ssl.sh yourdomain.com your@email.com

set -e

DOMAIN=$1
EMAIL=$2

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Использование: $0 <домен> <email>"
    echo "Пример: $0 cinema.example.com admin@example.com"
    exit 1
fi

echo "=== Шаг 1: Запускаем nginx + web для HTTP challenge ==="
docker compose -f docker-compose.prod.yml up -d nginx web db

echo "=== Шаг 2: Получаем сертификат ==="
docker compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path /var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN"

echo "=== Шаг 3: Создаём SSL-конфиг nginx ==="
sed "s/YOURDOMAIN.COM/$DOMAIN/g" nginx/conf.d/ssl.conf.template > nginx/conf.d/ssl.conf
# Убираем default.conf, чтобы не было конфликта
rm -f nginx/conf.d/default.conf

echo "=== Шаг 4: Перезапускаем nginx с SSL ==="
docker compose -f docker-compose.prod.yml restart nginx

echo ""
echo "=== Готово! ==="
echo "Сайт доступен по https://$DOMAIN"
echo "Mini App URL для @BotFather: https://$DOMAIN/telegram/"
