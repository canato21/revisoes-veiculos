from django.db import models
from django.core.validators import RegexValidator 

class Pessoa(models.Model):
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    cpf_validador = RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$')
    cpf = models.CharField(max_length=14, unique=True, validators=[cpf_validador])
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'alisson\".\"pessoas'
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'


class Veiculo(models.Model):
    proprietario = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='veiculos')
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    placa = models.CharField(max_length=10, unique=True)
    cor = models.CharField(max_length=30)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'

    class Meta:
        db_table = 'alisson\".\"veiculos'
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'


class Revisao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='revisoes')
    data_revisao = models.DateField()
    kilometragem = models.IntegerField()
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    oficina = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Revisão {self.veiculo} - {self.data_revisao}'

    class Meta:
        db_table = 'alisson\".\"revisoes'
        verbose_name = 'Revisão'
        verbose_name_plural = 'Revisões'