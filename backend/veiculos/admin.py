from django.contrib import admin
from .models import Pessoa, Veiculo, Revisao

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'sexo', 'data_nascimento']
    search_fields = ['nome', 'cpf', 'email']

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'placa', 'ano', 'proprietario']
    search_fields = ['placa', 'marca', 'modelo']

@admin.register(Revisao)
class RevisaoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'data_revisao', 'kilometragem', 'valor', 'oficina']
    search_fields = ['veiculo__placa']