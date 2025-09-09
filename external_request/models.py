from django.db import models


class RequestLog(models.Model):
    # Request
    request_payload = models.JSONField(blank=True, null=True, verbose_name="Тело Ззапроса")
    request_url = models.TextField(verbose_name="URL")
    request_method = models.CharField(max_length=32, verbose_name="Метод запроса")
    request_headers = models.JSONField(blank=True, null=True, verbose_name="Заголовки запроса")

    # Response
    response_data = models.JSONField(blank=True, null=True, verbose_name="Тело ответа")
    response_status_code = models.IntegerField(null=True, verbose_name="Статус ответа")
    response_headers = models.JSONField(null=True, blank=True, verbose_name="Заголовки ответа")
    request_query_params = models.JSONField(blank=True, null=True, verbose_name="Параметры запроса")

    # Time
    request_timestamp = models.DateTimeField(verbose_name="Время запроса", db_index=True)
    response_timestamp = models.DateTimeField(verbose_name="Время ответа")

    message = models.TextField(blank=True, verbose_name="Дополнительное описание")

    def __str__(self):
        return f"Request Log #{self.id}"

    class Meta:
        verbose_name = "Лог внешнего запроса"
        verbose_name_plural = "Логи внешних запросов"
