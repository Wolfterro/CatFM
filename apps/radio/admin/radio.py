from django.contrib import admin

from apps.radio.models import Radio


# Register your models here.
# ==========================
class RadioAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'identifier', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    ordering = ('name', 'created_at', 'updated_at')

    class Meta:
        model = Radio


admin.site.register(Radio, RadioAdmin)
