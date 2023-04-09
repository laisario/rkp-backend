from django.contrib import admin
from .models import Calibracao, Certificado, Criterio, Laboratorio, OrdemDeServico, Referencia, Resultado, Status


@admin.register(Calibracao)
class CalibracaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrumento', 'resultado')


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero')


@admin.register(Criterio)
class CriterioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'referencia')


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(OrdemDeServico)
class OrdemDeServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
