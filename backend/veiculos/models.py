"""
Cada classe aqui representa uma tabela no PostgreSQL.
O Django converte automaticamente estas classes em SQL através do ORM
(Object-Relational Mapping). O comando `python manage.py migrate`
executa esse SQL e cria/atualiza as tabelas no banco.
"""

from django.db import models
from django.core.validators import RegexValidator


# Validador de CPF criado fora da classe para poder ser reutilizado.
# RegexValidator verifica se o valor bate com a expressão regular.
# O pipe | significa OU — aceita qualquer um dos dois formatos:
#   - '^\d{3}\.\d{3}\.\d{3}-\d{2}$'  → formato: 123.456.789-00
#   - '^\d{11}$'                       → formato: 12345678900 (só números)
cpf_validador = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$'
)

class Pessoa(models.Model):
    """
    Representa um proprietário de veículo.
    Tabela no banco: alisson.pessoas
    """

    # Choices limita os valores aceitos pelo campo sexo
    # Formato: (valor_salvo_no_banco, texto_legível_para_humanos)
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    # CharField: campo de texto com tamanho máximo definido
    nome = models.CharField(max_length=100)

    # EmailField: valida automaticamente o formato de e-mail (precisa ter @)
    # unique=True: o banco rejeita dois registros com o mesmo e-mail
    email = models.EmailField(unique=True)

    # Validando CEP
    cep = models.CharField(max_length=9, default='----')
    rua    = models.CharField(max_length=200, blank=True, default='')
    bairro = models.CharField(max_length=100, blank=True, default='')
    numero = models.CharField(max_length=20,  blank=True, default='')
    cidade = models.CharField(max_length=100, blank=True, default='')
    estado = models.CharField(max_length=2,   blank=True, default='')

    telefone = models.CharField(max_length=20)

    # validators=[]: lista de validadores executados antes de salvar
    # O cpf_validador garante que o formato está correto
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[cpf_validador]
    )

    # DateField: armazena apenas data (sem horário)
    data_nascimento = models.DateField()

    # choices=SEXO_CHOICES: só aceita 'M' ou 'F'
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    # auto_now_add=True: preenchido automaticamente com a data/hora atual
    # na criação do registro. Nunca é alterado depois.
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Define como o objeto aparece como texto (ex: no painel admin)
        return self.nome

    class Meta:
        # db_table: nome real da tabela no PostgreSQL
        # A sintaxe com \" é necessária por causa do ponto no schema.tabela
        db_table = 'alisson\".\"pessoas'
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'


class Veiculo(models.Model):
    """
    Representa um veículo pertencente a uma Pessoa.
    Tabela no banco: alisson.veiculos
    Relacionamento: muitos veículos para uma pessoa (N:1)
    """

    # ForeignKey: cria a relação com a tabela Pessoa
    # on_delete=CASCADE: se a pessoa for deletada, seus veículos também são
    # related_name='veiculos': permite acessar os veículos de uma pessoa
    #   via: pessoa_obj.veiculos.all()
    proprietario = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='veiculos'
    )

    marca  = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)

    # IntegerField: número inteiro (sem casas decimais)
    ano = models.IntegerField()

    placa     = models.CharField(max_length=10, unique=True)
    cor       = models.CharField(max_length=30)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # f-string: texto formatado com variáveis embutidas
        return f'{self.marca} {self.modelo} - {self.placa}'

    class Meta:
        db_table = 'alisson\".\"veiculos'
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'


class Revisao(models.Model):
    """
    Representa uma revisão realizada em um Veículo.
    Tabela no banco: alisson.revisoes
    Relacionamento: muitas revisões para um veículo (N:1)
    """

    # ForeignKey para Veiculo — revisão pertence a um veículo
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='revisoes'
    )

    data_revisao = models.DateField()

    # IntegerField para quilometragem (sem decimais)
    kilometragem = models.IntegerField()

    # TextField: texto sem limite de tamanho (diferente do CharField)
    descricao = models.TextField()

    # DecimalField: número decimal preciso (evita erros de ponto flutuante do float)
    # max_digits=10: máximo 10 dígitos no total (incluindo decimais)
    # decimal_places=2: 2 casas decimais (centavos)
    # Suporta valores de -99999999.99 até 99999999.99
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    oficina   = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Revisão {self.veiculo} - {self.data_revisao}'

    class Meta:
        db_table = 'alisson\".\"revisoes'
        verbose_name = 'Revisão'
        verbose_name_plural = 'Revisões'
