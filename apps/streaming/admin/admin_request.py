from django.contrib import admin

from apps.streaming.models import AdminRequest


class AdminRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('status', 'created_at', 'updated_at')
    ordering = ('status', 'created_at', 'updated_at')

    readonly_fields = ('link_status_description', 'status', )

    class Meta:
        model = AdminRequest


admin.site.register(AdminRequest, AdminRequestAdmin)
