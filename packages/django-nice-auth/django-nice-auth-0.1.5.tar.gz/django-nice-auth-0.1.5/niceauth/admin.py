# niceauth/admin.py

from django.contrib import admin
from .models import NiceAuthRequest, NiceAuthResult


class NiceAuthResultInline(admin.StackedInline):
    model = NiceAuthResult
    can_delete = False
    verbose_name_plural = 'Nice Auth Results'
    readonly_fields = ('result', 'created_at', 'updated_at')


@admin.register(NiceAuthRequest)
class NiceAuthRequestAdmin(admin.ModelAdmin):
    list_display = ('request_no', 'created_at', 'updated_at', 'return_url', 'authtype', 'popupyn')
    search_fields = ('request_no', 'return_url', 'authtype', 'popupyn')
    list_filter = ('authtype', 'popupyn', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('request_no', 'enc_data', 'integrity_value', 'token_version_id', 'key', 'iv', 'return_url', 'authtype', 'popupyn')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    inlines = [NiceAuthResultInline]


@admin.register(NiceAuthResult)
class NiceAuthResultAdmin(admin.ModelAdmin):
    list_display = ('request', 'created_at', 'updated_at')
    search_fields = ('request__request_no',)
    readonly_fields = ('result', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('request', 'result')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
