from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _

from .models import Cliente,  Empresa,  Unidade


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa', 'telefone')


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'razao_social', 'cnpj')


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


admin.site.unregister(Group)
admin.site.index_title = _('Painel Administrativo')
admin.site.site_header = _('RKP Metrologia')
admin.site.site_title = _('RKP Metrologia')