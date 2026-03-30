"""interface administrativa gerada automaticamente."""

from django.contrib import admin
from .models import Pessoa, Veiculo, Revisao

"""
    Configuração da tela de Pessoas no painel admin.
    @admin.register(Pessoa) registra este modelo no admin.
"""
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'sexo', 'data_nascimento']
    search_fields = ['nome', 'cpf', 'email']

"""
    Configuração da tela de veiculos no painel admin
"""
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'placa', 'ano', 'proprietario']
    search_fields = ['placa', 'marca', 'modelo']

"""
    Configuração da tela de revisões no painel admin
"""

@admin.register(Revisao)
class RevisaoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'data_revisao', 'kilometragem', 'valor', 'oficina']
    search_fields = ['veiculo__placa']