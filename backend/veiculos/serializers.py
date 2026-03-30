"""
Serializers fazem duas coisas:
  1. SERIALIZAÇÃO: convertem objetos Python (do banco) em JSON para enviar ao frontend
  2. DESSERIALIZAÇÃO: recebem JSON do frontend, validam e convertem em objetos Python
"""

from rest_framework import serializers
from .models import Pessoa, Veiculo, Revisao
import re


class PessoaSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Pessoa.
    Converte objetos Pessoa em JSON e valida dados recebidos do frontend.
    """

    class Meta:
        model = Pessoa       # qual Model este serializer representa
        fields = '__all__'   # inclui TODOS os campos do model no JSON

    def validate_cpf(self, value):
        """
        Validação customizada do campo CPF.
        O Django REST Framework chama automaticamente métodos com o padrão
        validate_NOMECAMPO(self, value) antes de salvar.
        'value' é o CPF enviado pelo frontend.
        """

        # re.search: procura o padrão em qualquer parte da string
        # r'[a-zA-Z]' = qualquer letra maiúscula ou minúscula
        if re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError('O CPF não pode conter letras')

        # re.sub: substitui o padrão pelo segundo argumento
        # '[^0-9]' = qualquer caractere que NÃO seja dígito numérico, ou seja, remove pontos e traços
        # '' = substitui por vazio (remove todos os não-dígitos)
        cpf_numeros = re.sub(r'[^0-9]', '', value)

        if len(cpf_numeros) != 11:
            raise serializers.ValidationError(
                'O CPF deve conter exatamente 11 dígitos numéricos.'
            )

        # Sempre retorne o value ao final da validação
        # Você pode retornar o valor modificado (ex: formatado) se quiser
        return value

    def validate_cep(self, value):
        
        if re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError('O cep não pode conter letrar')
        
        cep_numero = re.sub(r'[^0-9]', '', value)

        if len(cep_numero) != 8:
            raise serializers.ValidationError('O cep deve ter exatamente 8 dígitos')
        
        return cep_numero

        


class VeiculoSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Veiculo.
    Adiciona o campo 'proprietario_nome' que não existe no model mas
    é calculado a partir da relação com Pessoa.
    """

    # Campo extra: não existe no Model, mas é calculado a partir dele.
    # source='proprietario.nome': navega pela relação FK para pegar o nome
    # read_only=True: este campo é enviado na resposta (GET) mas
    #                 não é aceito como entrada (POST/PUT)
    proprietario_nome = serializers.CharField(
        source='proprietario.nome',
        read_only=True
    )

    class Meta:
        model = Veiculo
        fields = '__all__'
        # '__all__' inclui 'proprietario_nome' pois foi declarado explicitamente acima


class RevisaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Revisao.
    Adiciona campos extras para facilitar o frontend — sem estes campos,
    o frontend receberia apenas 'veiculo: 3' (o ID numérico).
    Com eles, recebe também a placa, modelo e nome do proprietário.
    """

    # Atravessa uma relação: revisao → veiculo → placa
    veiculo_placa = serializers.CharField(
        source='veiculo.placa',
        read_only=True
    )

    # Atravessa uma relação: revisao → veiculo → modelo
    veiculo_modelo = serializers.CharField(
        source='veiculo.modelo',
        read_only=True
    )

    # Atravessa DUAS relações: revisao → veiculo → proprietario → nome
    proprietario_nome = serializers.CharField(
        source='veiculo.proprietario.nome',
        read_only=True
    )

    class Meta:
        model = Revisao
        fields = '__all__'
