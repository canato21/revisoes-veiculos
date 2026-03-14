"""
Script de geração de dados de teste para o sistema de revisões de veículos.
Gera dados realistas e variados para testar todos os relatórios.
Execute dentro do venv na pasta backend:
    python popular_banco.py
"""

import os
import sys
import django
import random
from datetime import date, timedelta
from decimal import Decimal

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from veiculos.models import Pessoa, Veiculo, Revisao

# ── DADOS PARA GERAÇÃO ────────────────────────────────────────────────────────

NOMES_MASCULINOS = [
    "Alisson Ferreira", "Carlos Eduardo", "João Pedro", "Lucas Oliveira",
    "Gabriel Santos", "Rafael Lima", "Mateus Costa", "Felipe Souza",
    "Bruno Martins", "Thiago Alves", "Anderson Silva", "Rodrigo Pereira",
    "Marcelo Rocha", "Leonardo Gomes", "Diego Mendes", "Gustavo Barbosa",
    "Henrique Carvalho", "Vinicius Ribeiro", "Patrick Araújo", "Samuel Nunes",
]

NOMES_FEMININOS = [
    "Ana Carolina", "Maria Eduarda", "Juliana Freitas", "Fernanda Castro",
    "Camila Rodrigues", "Beatriz Nascimento", "Larissa Cardoso", "Priscila Moura",
    "Vanessa Cunha", "Tatiane Pires", "Leticia Monteiro", "Gabriela Teixeira",
    "Renata Lopes", "Sabrina Vieira", "Adriana Correia", "Patricia Dias",
    "Cristina Faria", "Simone Borges", "Danielle Ramos", "Elaine Sousa",
]

MARCAS_MODELOS = {
    "Toyota":     ["Corolla", "Hilux", "Yaris", "RAV4", "Etios", "Camry"],
    "Honda":      ["Civic", "Fit", "HR-V", "City", "CR-V", "WR-V"],
    "Chevrolet":  ["Onix", "Tracker", "S10", "Cruze", "Spin", "Equinox"],
    "Volkswagen": ["Gol", "Polo", "T-Cross", "Virtus", "Tiguan", "Saveiro"],
    "Ford":       ["Ka", "EcoSport", "Ranger", "Territory", "Bronco Sport"],
    "Hyundai":    ["HB20", "Creta", "Tucson", "i30", "Santa Fe"],
    "Fiat":       ["Argo", "Cronos", "Pulse", "Toro", "Strada", "Uno"],
    "Renault":    ["Kwid", "Sandero", "Logan", "Duster", "Captur"],
    "Jeep":       ["Renegade", "Compass", "Commander", "Wrangler"],
    "Nissan":     ["Kicks", "Versa", "Frontier", "March", "Sentra"],
}

CORES = [
    "Branco", "Preto", "Prata", "Cinza", "Vermelho",
    "Azul", "Verde", "Bege", "Marrom", "Dourado",
]

OFICINAS = [
    "Auto Center Silva", "Mecânica do João", "Garage Premium",
    "Centro Automotivo Dourados", "Oficina Souza & Filhos",
    "Auto Service Alisson", "Revisão Express", "Mecânica Confiança",
    "Auto Peças e Serviços MS", "Garage Tech",
]

DESCRICOES_REVISAO = [
    "Troca de óleo e filtro",
    "Revisão completa dos freios",
    "Alinhamento e balanceamento",
    "Troca de pastilhas de freio",
    "Revisão do sistema de arrefecimento",
    "Troca de correia dentada",
    "Revisão elétrica completa",
    "Troca de velas e cabos",
    "Revisão da suspensão dianteira",
    "Troca de amortecedores traseiros",
    "Revisão do câmbio automático",
    "Limpeza de bicos injetores",
    "Troca de filtro de ar e cabine",
    "Revisão geral com 10.000 km",
    "Revisão geral com 20.000 km",
    "Revisão geral com 30.000 km",
    "Troca de fluido de freio",
    "Revisão do sistema de direção",
    "Diagnóstico eletrônico completo",
    "Troca de bateria",
]

# ── FUNÇÕES AUXILIARES ─────────────────────────────────────────────────────────

def gerar_cpf():
    """Gera um CPF formatado único."""
    while True:
        nums = [random.randint(0, 9) for _ in range(11)]
        cpf = f"{nums[0]}{nums[1]}{nums[2]}.{nums[3]}{nums[4]}{nums[5]}.{nums[6]}{nums[7]}{nums[8]}-{nums[9]}{nums[10]}"
        if not Pessoa.objects.filter(cpf=cpf).exists():
            return cpf

def gerar_email(nome):
    """Gera um email baseado no nome."""
    dominios = ["gmail.com", "hotmail.com", "yahoo.com.br", "outlook.com", "email.com"]
    nome_limpo = nome.lower().replace(" ", ".").replace("ã","a").replace("é","e").replace("ê","e").replace("ó","o").replace("ú","u").replace("ç","c").replace("á","a").replace("â","a").replace("í","i")
    sufixo = random.randint(1, 999)
    while True:
        email = f"{nome_limpo}{sufixo}@{random.choice(dominios)}"
        if not Pessoa.objects.filter(email=email).exists():
            return email

def gerar_telefone():
    """Gera um telefone celular do MS."""
    numero = random.randint(90000000, 99999999)
    return f"(67) 9{numero}"

def gerar_placa():
    """Gera uma placa no formato Mercosul ou antigo."""
    while True:
        if random.random() > 0.5:
            # Formato Mercosul: ABC1D23
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            num1 = random.randint(0, 9)
            letra_meio = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            num2 = random.randint(0, 9)
            num3 = random.randint(0, 9)
            placa = f"{letras}{num1}{letra_meio}{num2}{num3}"
        else:
            # Formato antigo: ABC-1234
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            numeros = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            placa = f"{letras}-{numeros}"
        if not Veiculo.objects.filter(placa=placa).exists():
            return placa

def gerar_data_nascimento(sexo):
    """Gera data de nascimento realista (18 a 70 anos)."""
    hoje = date.today()
    anos = random.randint(18, 70)
    dias_extras = random.randint(0, 365)
    return hoje - timedelta(days=anos*365 + dias_extras)

def gerar_revisoes_para_veiculo(veiculo, quantidade):
    """Gera revisões com datas progressivas e KM crescente."""
    hoje = date.today()
    # Data da primeira revisão: entre 1 e 4 anos atrás
    data_atual = hoje - timedelta(days=random.randint(365, 4*365))
    km_atual = random.randint(5000, 20000)

    revisoes_criadas = 0
    for _ in range(quantidade):
        descricao = random.choice(DESCRICOES_REVISAO)
        valor = Decimal(str(round(random.uniform(150, 2500), 2)))
        oficina = random.choice(OFICINAS)

        Revisao.objects.create(
            veiculo=veiculo,
            data_revisao=data_atual,
            kilometragem=km_atual,
            descricao=descricao,
            valor=valor,
            oficina=oficina,
        )
        revisoes_criadas += 1

        # Avança entre 45 e 180 dias para a próxima revisão
        intervalo = random.randint(45, 180)
        data_atual += timedelta(days=intervalo)
        km_atual += random.randint(3000, 15000)

        # Não gera revisões futuras
        if data_atual > hoje:
            break

    return revisoes_criadas

# ── MAIN ──────────────────────────────────────────────────────────────────────

def popular():
    print("=" * 60)
    print("  POPULANDO O BANCO DE DADOS")
    print("=" * 60)

    # Limpa dados existentes
    print("\n🗑️  Limpando dados existentes...")
    Revisao.objects.all().delete()
    Veiculo.objects.all().delete()
    Pessoa.objects.all().delete()
    print("   Dados anteriores removidos.")

    # ── PESSOAS ──────────────────────────────────────────────────────
    print("\n👤 Criando pessoas...")
    pessoas = []

    # 20 homens
    nomes_m = random.sample(NOMES_MASCULINOS, 20)
    for nome in nomes_m:
        p = Pessoa.objects.create(
            nome=nome,
            email=gerar_email(nome),
            telefone=gerar_telefone(),
            cpf=gerar_cpf(),
            data_nascimento=gerar_data_nascimento('M'),
            sexo='M',
        )
        pessoas.append(p)

    # 20 mulheres
    nomes_f = random.sample(NOMES_FEMININOS, 20)
    for nome in nomes_f:
        p = Pessoa.objects.create(
            nome=nome,
            email=gerar_email(nome),
            telefone=gerar_telefone(),
            cpf=gerar_cpf(),
            data_nascimento=gerar_data_nascimento('F'),
            sexo='F',
        )
        pessoas.append(p)

    print(f"   ✅ {Pessoa.objects.count()} pessoas criadas (20 homens + 20 mulheres)")

    # ── VEÍCULOS ─────────────────────────────────────────────────────
    print("\n🚗 Criando veículos...")
    veiculos = []

    marcas = list(MARCAS_MODELOS.keys())

    for pessoa in pessoas:
        # Distribui: algumas pessoas com 1 veículo, outras com 2 ou 3
        qtd = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
        for _ in range(qtd):
            marca = random.choice(marcas)
            modelo = random.choice(MARCAS_MODELOS[marca])
            ano = random.randint(2010, 2024)
            v = Veiculo.objects.create(
                proprietario=pessoa,
                marca=marca,
                modelo=modelo,
                ano=ano,
                placa=gerar_placa(),
                cor=random.choice(CORES),
            )
            veiculos.append(v)

    print(f"   ✅ {Veiculo.objects.count()} veículos criados")

    # ── REVISÕES ─────────────────────────────────────────────────────
    print("\n🔧 Criando revisões...")
    total_revisoes = 0

    for veiculo in veiculos:
        # Entre 2 e 8 revisões por veículo
        qtd = random.randint(2, 8)
        total_revisoes += gerar_revisoes_para_veiculo(veiculo, qtd)

    print(f"   ✅ {Revisao.objects.count()} revisões criadas")

    # ── RESUMO ───────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RESUMO FINAL")
    print("=" * 60)
    print(f"  👥 Pessoas:  {Pessoa.objects.count():>5} (homens: {Pessoa.objects.filter(sexo='M').count()}, mulheres: {Pessoa.objects.filter(sexo='F').count()})")
    print(f"  🚗 Veículos: {Veiculo.objects.count():>5}")
    print(f"  🔧 Revisões: {Revisao.objects.count():>5}")
    print()

    # Estatísticas extras
    from django.db.models import Count, Avg
    print("  📊 Marcas mais frequentes:")
    marcas_count = Veiculo.objects.values('marca').annotate(total=Count('id')).order_by('-total')[:5]
    for m in marcas_count:
        print(f"     {m['marca']:<15} {m['total']} veículos")

    print()
    print("  📊 Pessoas com mais veículos:")
    top_pessoas = Pessoa.objects.annotate(total=Count('veiculos')).order_by('-total')[:5]
    for p in top_pessoas:
        print(f"     {p.nome:<25} {p.total} veículos")

    print()
    print("  📊 Oficinas mais usadas:")
    top_oficinas = Revisao.objects.values('oficina').annotate(total=Count('id')).order_by('-total')[:5]
    for o in top_oficinas:
        print(f"     {o['oficina']:<30} {o['total']} revisões")

    print()
    print("=" * 60)
    print("  ✅ Banco populado com sucesso!")
    print("  Agora teste os endpoints:")
    print("  http://localhost:8000/api/pessoas/")
    print("  http://localhost:8000/api/veiculos/por-marca/")
    print("  http://localhost:8000/api/revisoes/proximas-revisoes/")
    print("=" * 60)

if __name__ == '__main__':
    popular()