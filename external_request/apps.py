from django.apps import AppConfig


class RequestsLoggerConfig(AppConfig):
    name = "external_request"
    verbose_name = "Запросы во внешние сервисы"
