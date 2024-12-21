from django.contrib import admin

from apps.catuser.models import CatUser

# Register your models here.
# ==========================
class CatUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CatUser, CatUserAdmin)
