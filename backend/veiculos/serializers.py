from rest_framework import serializers
from .models import Pessoa, Veiculo, Revisao
import re


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'

    def validade_cpf(self, value):
        if re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("O cpf não pode conter letras")
        
        cpf_numeros = re.sub(r'[^0-9]', '', value)

        if len(cpf_numeros) != 11:
            raise serializers.ValidationError("O cpf deve conter exatamente 11 dígitos numéricos.")

        return value
        
class VeiculoSerializer(serializers.ModelSerializer):
    proprietario_nome = serializers.CharField(
        source='proprietario.nome', read_only=True
    )

    class Meta:
        model = Veiculo
        fields = '__all__'


class RevisaoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(
        source='veiculo.placa', read_only=True
    )
    veiculo_modelo = serializers.CharField(
        source='veiculo.modelo', read_only=True
    )
    proprietario_nome = serializers.CharField(
        source='veiculo.proprietario.nome', read_only=True
    )

    class Meta:
        model = Revisao
        fields = '__all__'