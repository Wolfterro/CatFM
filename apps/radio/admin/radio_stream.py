from django.contrib import admin
from rest_framework.authtoken.models import Token

from apps.radio.models import RadioStream
from apps.radio.services import BroacastListenerService
from apps.radio.admin.actions.radio_stream import start_broadcasts, stop_broadcasts


class RadioStreamAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_radio_stream_change_list.html"

    list_display = ('title', 'radio', 'identifier', 'created_at', 'updated_at')
    search_fields = ('radio', 'identifier', 'title', 'created_at', 'updated_at')
    list_filter = ('radio', 'created_at', 'updated_at')
    ordering = ('radio', 'title', 'created_at', 'updated_at')

    actions = [start_broadcasts, stop_broadcasts, ]

    def changelist_view(self, request, extra_context=None):
        # Dados adicionais que você quer passar para o template
        listener = BroacastListenerService()
        token = Token.objects.filter(user=request.user).first()
        if token:
            token = token.key

        custom_data = {
            'broadcasts': listener.get_active_broadcasts(),
            'token': token
        }

        # Combine os dados extras com o contexto existente
        extra_context = extra_context or {}
        extra_context.update(custom_data)
        print(extra_context)

        # Chama a implementação padrão com o contexto atualizado
        return super().changelist_view(request, extra_context=extra_context)

    class Meta:
        model = RadioStream


admin.site.register(RadioStream, RadioStreamAdmin)
