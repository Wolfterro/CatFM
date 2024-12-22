from django.contrib import admin

from apps.radio.models import Radio, RadioStream


# Register your models here.
# ==========================
class RadioAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'identifier', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    ordering = ('name', 'created_at', 'updated_at')

    class Meta:
        model = Radio


class RadioStreamAdmin(admin.ModelAdmin):
    list_display = ('radio', 'identifier', 'title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('radio', 'identifier', 'title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('radio', 'is_active', 'created_at', 'updated_at')
    ordering = ('radio', 'title', 'is_active', 'created_at', 'updated_at')

    class Meta:
        model = RadioStream


admin.site.register(Radio, RadioAdmin)
admin.site.register(RadioStream, RadioStreamAdmin)
