"""
Script de geração de dados de teste — versão atualizada.
Preenche todos os campos do sistema atual:
  - Pessoas: CEP (8 dígitos sem traço), rua, bairro, número, cidade, estado
  - Veículos: cor em hex (compatível com color picker do frontend)
  - Revisões: KM e datas sempre crescentes (nunca violam a validação de ordem)

Execução dentro do Docker (recomendado):
    docker exec -it revisoes_veiculos-backend-1 python popular_banco.py

Ou no venv local (pasta backend):
    python popular_banco.py
"""

import os
import django
import random
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from veiculos.models import Pessoa, Veiculo, Revisao

# ── NOMES ─────────────────────────────────────────────────────────────────────

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

# ── VEÍCULOS ──────────────────────────────────────────────────────────────────

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

# Cores em hex — mesmas do frontend (Veiculos.vue / Pessoas.vue)
# O frontend identifica pelo valor hex e exibe o nome correspondente
CORES_HEX = [
    "#FFFFFF",  # Branco
    "#1a1a1a",  # Preto
    "#C0C0C0",  # Prata
    "#808080",  # Cinza
    "#CC0000",  # Vermelho
    "#1a4fa0",  # Azul
    "#4fc3f7",  # Azul Claro
    "#2e7d32",  # Verde
    "#f9a825",  # Amarelo
    "#e65100",  # Laranja
    "#5d4037",  # Marrom
    "#d7b899",  # Bege
    "#c8a84b",  # Dourado
]

# ── ENDEREÇOS — CEP sem traço, cidades do MS ──────────────────────────────────

ENDERECOS = [
    {"cep": "79800001", "rua": "Rua Coronel Ponciano",      "bairro": "Centro",              "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79800010", "rua": "Avenida Marcelino Pires",   "bairro": "Centro",              "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79801001", "rua": "Rua João Rosa Pires",       "bairro": "Jardim Caramuru",     "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79802001", "rua": "Rua Onze de Outubro",       "bairro": "Vila Planalto",       "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79803001", "rua": "Rua Monte Alegre",          "bairro": "Jardim América",      "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79804001", "rua": "Rua Bela Vista",            "bairro": "Jardim Guaicurus",    "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79805001", "rua": "Rua dos Pinheiros",         "bairro": "Vila Rosa",           "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79806001", "rua": "Rua Hayel Bon Faker",       "bairro": "Jardim Clímax",       "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79807001", "rua": "Rua Toshinobu Katayama",    "bairro": "Altos do Indaiá",     "cidade": "Dourados",      "estado": "MS"},
    {"cep": "79808001", "rua": "Rua Weimar Gonçalves",      "bairro": "Parque Nova Dourados","cidade": "Dourados",      "estado": "MS"},
    {"cep": "79824001", "rua": "Rua Oliveira Marques",      "bairro": "Centro",              "cidade": "Douradina",     "estado": "MS"},
    {"cep": "79960001", "rua": "Rua 13 de Maio",            "bairro": "Centro",              "cidade": "Ponta Porã",    "estado": "MS"},
    {"cep": "79750001", "rua": "Avenida Central",           "bairro": "Centro",              "cidade": "Maracaju",      "estado": "MS"},
    {"cep": "79730001", "rua": "Rua Rui Barbosa",           "bairro": "Centro",              "cidade": "Itaporã",       "estado": "MS"},
    {"cep": "79760001", "rua": "Rua Benjamin Constant",     "bairro": "Centro",              "cidade": "Rio Brilhante", "estado": "MS"},
    {"cep": "79400001", "rua": "Rua 7 de Setembro",         "bairro": "Centro",              "cidade": "Corumbá",       "estado": "MS"},
    {"cep": "79002001", "rua": "Avenida Afonso Pena",       "bairro": "Centro",              "cidade": "Campo Grande",  "estado": "MS"},
    {"cep": "79004001", "rua": "Rua 14 de Julho",           "bairro": "Centro",              "cidade": "Campo Grande",  "estado": "MS"},
    {"cep": "79005001", "rua": "Rua Dom Aquino",            "bairro": "Centro",              "cidade": "Campo Grande",  "estado": "MS"},
    {"cep": "79006001", "rua": "Rua Marechal Rondon",       "bairro": "Monte Castelo",       "cidade": "Campo Grande",  "estado": "MS"},
]

# ── REVISÕES ──────────────────────────────────────────────────────────────────

OFICINAS = [
    "Auto Center Silva",
    "Mecânica do João",
    "Garage Premium",
    "Centro Automotivo Dourados",
    "Oficina Souza & Filhos",
    "Auto Service Alisson",
    "Revisão Express",
    "Mecânica Confiança",
    "Auto Peças e Serviços MS",
    "Garage Tech",
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
    """Gera CPF válido com dígitos verificadores corretos e único no banco."""
    def calcular_digito(nums):
        s = sum(v * (len(nums) + 1 - i) for i, v in enumerate(nums))
        r = 11 - (s % 11)
        return 0 if r >= 10 else r

    while True:
        base = [random.randint(0, 9) for _ in range(9)]
        # Rejeita sequências repetidas (ex: 111.111.111-11)
        if len(set(base)) == 1:
            continue
        d1 = calcular_digito(base)
        d2 = calcular_digito(base + [d1])
        nums = base + [d1, d2]
        cpf = (
            f"{nums[0]}{nums[1]}{nums[2]}."
            f"{nums[3]}{nums[4]}{nums[5]}."
            f"{nums[6]}{nums[7]}{nums[8]}-"
            f"{nums[9]}{nums[10]}"
        )
        if not Pessoa.objects.filter(cpf=cpf).exists():
            return cpf


def gerar_email(nome):
    """Email único baseado no nome, sem acentos."""
    trocas = str.maketrans(
        "áàãâäéèêëíìîïóòõôöúùûüçñÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ",
        "aaaaaeeeeiiiiooooouuuucnAAAAAEEEEIIIIOOOOOUUUUCN"
    )
    dominios = ["gmail.com", "hotmail.com", "yahoo.com.br", "outlook.com"]
    base = nome.lower().translate(trocas).replace(" ", ".")
    while True:
        email = f"{base}{random.randint(1, 999)}@{random.choice(dominios)}"
        if not Pessoa.objects.filter(email=email).exists():
            return email


def gerar_telefone():
    """Telefone celular com DDD 67 (Mato Grosso do Sul)."""
    return f"(67) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}"


def gerar_placa():
    """Placa no formato Mercosul (ABC1D23) ou antigo (ABC-1234), única no banco."""
    while True:
        if random.random() > 0.4:
            # Mercosul
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            placa = f"{letras}{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0,9)}{random.randint(0,9)}"
        else:
            # Antigo
            letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            placa = f"{letras}-{''.join(str(random.randint(0,9)) for _ in range(4))}"
        if not Veiculo.objects.filter(placa=placa).exists():
            return placa


def gerar_numero_residencia():
    """Número de residência: só dígitos, máx 10 chars (igual à validação do frontend)."""
    return str(random.randint(1, 9999))


def gerar_data_nascimento():
    """Data de nascimento entre 18 e 70 anos atrás."""
    hoje = date.today()
    dias = random.randint(18 * 365, 70 * 365) + random.randint(0, 364)
    return hoje - timedelta(days=dias)


def gerar_revisoes_para_veiculo(veiculo, quantidade):
    """
    Gera revisões com datas e KM SEMPRE crescentes.
    Respeita a validação do ModalRevisao.vue:
      - data_revisao nunca pode ser < última revisão
      - kilometragem nunca pode ser < última revisão
      - data nunca pode ser futura
    """
    hoje = date.today()
    data_atual = hoje - timedelta(days=random.randint(400, 4 * 365))
    km_atual = random.randint(5000, 20000)

    criadas = 0
    for _ in range(quantidade):
        if data_atual >= hoje:
            break

        Revisao.objects.create(
            veiculo=veiculo,
            data_revisao=data_atual,
            kilometragem=km_atual,
            descricao=random.choice(DESCRICOES_REVISAO),
            valor=Decimal(str(round(random.uniform(150.0, 2500.0), 2))),
            oficina=random.choice(OFICINAS),
        )
        criadas += 1

        # Avança data: +45 a +180 dias (sempre crescente)
        data_atual += timedelta(days=random.randint(45, 180))
        # Avança KM: +3000 a +15000 (sempre crescente)
        km_atual += random.randint(3000, 15000)

    return criadas


# ── MAIN ──────────────────────────────────────────────────────────────────────

def popular():
    print("=" * 60)
    print("  POPULANDO O BANCO DE DADOS")
    print("=" * 60)

    # Limpa tudo
    print("\n🗑️  Limpando dados existentes...")
    Revisao.objects.all().delete()
    Veiculo.objects.all().delete()
    Pessoa.objects.all().delete()
    print("   Dados anteriores removidos.")

    # ── PESSOAS ──────────────────────────────────────────────────────
    print("\n👤 Criando pessoas...")
    pessoas = []

    for nome in random.sample(NOMES_MASCULINOS, 20):
        endereco = random.choice(ENDERECOS)
        p = Pessoa.objects.create(
            nome=nome,
            email=gerar_email(nome),
            telefone=gerar_telefone(),
            cpf=gerar_cpf(),
            data_nascimento=gerar_data_nascimento(),
            sexo='M',
            # Campos de endereço — CEP sem traço (8 dígitos, como o serializer salva)
            cep=endereco["cep"],
            rua=endereco["rua"],
            bairro=endereco["bairro"],
            numero=gerar_numero_residencia(),
            cidade=endereco["cidade"],
            estado=endereco["estado"],
        )
        pessoas.append(p)

    for nome in random.sample(NOMES_FEMININOS, 20):
        endereco = random.choice(ENDERECOS)
        p = Pessoa.objects.create(
            nome=nome,
            email=gerar_email(nome),
            telefone=gerar_telefone(),
            cpf=gerar_cpf(),
            data_nascimento=gerar_data_nascimento(),
            sexo='F',
            cep=endereco["cep"],
            rua=endereco["rua"],
            bairro=endereco["bairro"],
            numero=gerar_numero_residencia(),
            cidade=endereco["cidade"],
            estado=endereco["estado"],
        )
        pessoas.append(p)

    print(f"   ✅ {Pessoa.objects.count()} pessoas criadas "
          f"({Pessoa.objects.filter(sexo='M').count()} homens + "
          f"{Pessoa.objects.filter(sexo='F').count()} mulheres)")

    # ── VEÍCULOS ─────────────────────────────────────────────────────
    print("\n🚗 Criando veículos...")
    veiculos = []

    for pessoa in pessoas:
        qtd = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
        for _ in range(qtd):
            marca = random.choice(list(MARCAS_MODELOS.keys()))
            v = Veiculo.objects.create(
                proprietario=pessoa,
                marca=marca,
                modelo=random.choice(MARCAS_MODELOS[marca]),
                ano=random.randint(2010, 2024),
                placa=gerar_placa(),
                # Cor em hex — compatível com o color picker do frontend
                cor=random.choice(CORES_HEX),
            )
            veiculos.append(v)

    print(f"   ✅ {Veiculo.objects.count()} veículos criados")

    # ── REVISÕES ─────────────────────────────────────────────────────
    print("\n🔧 Criando revisões...")

    for veiculo in veiculos:
        gerar_revisoes_para_veiculo(veiculo, random.randint(2, 8))

    print(f"   ✅ {Revisao.objects.count()} revisões criadas")

    # ── RESUMO ───────────────────────────────────────────────────────
    from django.db.models import Count

    print("\n" + "=" * 60)
    print("  RESUMO FINAL")
    print("=" * 60)
    print(f"  👥 Pessoas:  {Pessoa.objects.count():>5}")
    print(f"  🚗 Veículos: {Veiculo.objects.count():>5}")
    print(f"  🔧 Revisões: {Revisao.objects.count():>5}")

    print("\n  📊 Marcas mais frequentes:")
    for m in Veiculo.objects.values('marca').annotate(t=Count('id')).order_by('-t')[:5]:
        print(f"     {m['marca']:<15} {m['t']} veículos")

    print("\n  📊 Pessoas com mais veículos:")
    for p in Pessoa.objects.annotate(t=Count('veiculos')).order_by('-t')[:5]:
        print(f"     {p.nome:<25} {p.t} veículos")

    print("\n  📊 Oficinas mais usadas:")
    for o in Revisao.objects.values('oficina').annotate(t=Count('id')).order_by('-t')[:5]:
        print(f"     {o['oficina']:<35} {o['t']} revisões")

    print("\n  📊 Cidades:")
    for c in Pessoa.objects.values('cidade').annotate(t=Count('id')).order_by('-t'):
        print(f"     {c['cidade']:<20} {c['t']} pessoas")

    print("\n" + "=" * 60)
    print("  ✅ Banco populado com sucesso!")
    print()
    print("  Para rodar dentro do Docker:")
    print("  docker exec -it revisoes_veiculos-backend-1 python popular_banco.py")
    print("=" * 60)


if __name__ == '__main__':
    popular()