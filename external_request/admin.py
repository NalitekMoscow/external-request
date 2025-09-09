from datetime import timedelta, date, datetime, time

from django.apps import apps
from django.contrib import admin
from django.contrib import admin
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import escape

from . import models


def week_start_for(d: date) -> date:
    # понедельник (iso Monday=1)
    return d - timedelta(days=d.isoweekday() - 1)


class WeekListFilter(admin.SimpleListFilter):
    title = "неделя"
    parameter_name = "week"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        dates = qs.dates("request_timestamp", "week", order="DESC")
        lookups = []
        for d in dates:
            week_start = d
            week_end = d + timedelta(days=6)
            label = f"{week_start.strftime('%d.%m.%Y')} – {week_end.strftime('%d.%m.%Y')}"
            lookups.append((week_start.isoformat(), label))
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            start = date.fromisoformat(self.value())
            end = start + timedelta(days=7)

            start_dt = timezone.make_aware(datetime.combine(start, time.min))
            end_dt   = timezone.make_aware(datetime.combine(end,   time.min))
            return queryset.filter(request_timestamp__gte=start_dt, request_timestamp__lt=end_dt)
        return queryset


class DateRedirectMixin:
    show_full_result_count = False
    def changelist_view(self, request, extra_context=None):
        if "week" not in request.GET:
            today = timezone.localdate()
            ws = week_start_for(today).isoformat()
            params = request.GET.copy()
            params["week"] = ws
            for k in list(params.keys()):
                if k.startswith("request_timestamp__"):
                    params.pop(k, None)
            return redirect(f"{request.path}?{params.urlencode()}")

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(models.RequestLog)
class RequestLogAdmin(DateRedirectMixin, admin.ModelAdmin):
    list_display = (
        "request_url",
        "request_method",
        "request_timestamp",
        "response_status_code",
        "response_timestamp",
    )
    list_filter = (
        WeekListFilter,
        "response_status_code",
        "request_method"
    )
    search_fields = ("request_url",)
    ordering = ("-request_timestamp",)

    def has_change_permission(self, request, obj=None):  # noqa
        return False

    def has_add_permission(self, request, obj=None):  # noqa
        return False

    def has_delete_permission(self, request, obj=None):  # noqa
        return False
