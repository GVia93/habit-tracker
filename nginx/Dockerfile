# Лёгкий актуальный образ Nginx
FROM nginx:1.25-alpine

# Точки монтирования для статики/медиа (под наши alias в nginx.conf)
RUN mkdir -p /app/staticfiles /app/media

# Кладём конфиг внутрь образа
COPY nginx.conf /etc/nginx/nginx.conf

# Порт HTTP
EXPOSE 80
