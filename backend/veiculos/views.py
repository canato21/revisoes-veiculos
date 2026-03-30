"""
views.py — Lógica dos endpoints da API

Views são responsáveis por processar as requisições HTTP e retornar respostas.
Usamos ViewSets do Django REST Framework, que agrupam todo o CRUD de um recurso
em uma única classe. O router (em urls.py) conecta cada ViewSet às suas URLs.

Cada ModelViewSet herda automaticamente 5 ações:
  list     → GET    /api/recurso/        — lista todos
  create   → POST   /api/recurso/        — cria um novo
  retrieve → GET    /api/recurso/{id}/   — busca um pelo ID
  update   → PUT    /api/recurso/{id}/   — atualiza completamente
  destroy  → DELETE /api/recurso/{id}/   — deleta

Além disso, usamos @action para criar endpoints customizados (relatórios).
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.db.models import Count
from django.db import connection
from datetime import date

from .models import Pessoa, Veiculo, Revisao
from .serializers import PessoaSerializer, VeiculoSerializer, RevisaoSerializer


class PessoaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Pessoa — gerencia todo o CRUD de pessoas.
    Endpoints gerados automaticamente:
      GET    /api/pessoas/       → lista todas as pessoas
      POST   /api/pessoas/       → cria uma pessoa
      GET    /api/pessoas/{id}/  → busca uma pessoa
      PUT    /api/pessoas/{id}/  → atualiza uma pessoa
      DELETE /api/pessoas/{id}/  → deleta uma pessoa
    """

    # queryset: consulta base que retorna todos os objetos
    # order_by('nome'): ordena alfabeticamente por nome
    queryset = Pessoa.objects.all().order_by('nome')

    # serializer_class: qual serializer usar para converter os dados
    serializer_class = PessoaSerializer 

    # Configuração de busca (SearchFilter)
    filter_backends = [SearchFilter]
    search_fields = ['nome', 'cpf', 'email', 'telefone']

    @action(detail=False, methods=['get'], url_path='por-sexo')
    def por_sexo(self, request):
        """
        Relatório: pessoas separadas por sexo com idade média.
        Endpoint: GET /api/pessoas/por-sexo/

        detail=False: a rota NÃO tem {id} → /api/pessoas/por-sexo/
        detail=True:  a rota TEM {id}     → /api/pessoas/{id}/por-sexo/
        """
        pessoas = Pessoa.objects.all()

        # Estrutura do resultado que será enviada ao frontend
        resultado = {
            'masculino': [],
            'feminino': [],
            'idade_media_m': 0,
            'idade_media_f': 0
        }

        idades_m = []
        idades_f = []
        hoje = date.today()

        for p in pessoas:
            # Calcula a idade subtraindo o ano de nascimento do ano atual
            idade = hoje.year - p.data_nascimento.year

            # Serializa o objeto Pessoa em dicionário Python
            dados = PessoaSerializer(p).data
            dados['idade'] = idade  # adiciona a idade calculada ao dicionário

            if p.sexo == 'M':
                resultado['masculino'].append(dados)
                idades_m.append(idade)
            else:
                resultado['feminino'].append(dados)
                idades_f.append(idade)

        # Calcula a média de idades (evita divisão por zero com o 'if')
        resultado['idade_media_m'] = round(sum(idades_m) / len(idades_m), 1) if idades_m else 0
        resultado['idade_media_f'] = round(sum(idades_f) / len(idades_f), 1) if idades_f else 0

        # Response(): retorna os dados como JSON com status 200
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='idade')
    def por_idade(self, request):
        """
        Relatório: busca pessoas que nasceram dentro de um período específico.
        Endpoint: GET /api/pessoas/idade/?inicio=YYYY-MM-DD&fim=YYYY-MM-DD
        """
        data_comeco = request.query_params.get('inicio')
        data_final = request.query_params.get('fim')

        pessoas = Pessoa.objects.all()

        # filter(): adiciona condições WHERE na consulta (>= e <=)
        if data_comeco:
            pessoas = pessoas.filter(data_nascimento__gte=data_comeco)
        if data_final:
            pessoas = pessoas.filter(data_nascimento__lte=data_final)

        return Response(PessoaSerializer(pessoas, many=True).data)


class VeiculoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Veiculo — gerencia todo o CRUD de veículos e relatórios associados.
    """

    # select_related('proprietario'): faz JOIN com a tabela pessoas.
    # Isso evita o problema N+1: sem select_related, para listar 100 veículos
    # o Django faria 100 consultas extras para buscar cada proprietário.
    queryset = Veiculo.objects.all().select_related('proprietario')
    serializer_class = VeiculoSerializer
    
    filter_backends = [SearchFilter]
    search_fields = ['marca', 'modelo', 'placa', 'proprietario__nome']

    def get_queryset(self):
        """
        Sobrescreve a busca padrão para permitir filtro por proprietário via URL.
        Ex: /api/veiculos/?proprietario=5
        """
        queryset = Veiculo.objects.all().select_related('proprietario')
        proprietario_id = self.request.query_params.get('proprietario')
        
        if proprietario_id:
            queryset = queryset.filter(proprietario_id=proprietario_id)
        
        return queryset

    @action(detail=False, methods=['get'], url_path='por-pessoa')
    def por_pessoa(self, request):
        """
        Relatório: todos os veículos agrupados por pessoa, ordenados por nome.
        Endpoint: GET /api/veiculos/por-pessoa/
        """
        # prefetch_related: carrega os veículos de cada pessoa de forma otimizada
        pessoas = Pessoa.objects.prefetch_related('veiculos').order_by('nome')

        resultado = []
        for p in pessoas:
            resultado.append({
                'pessoa': PessoaSerializer(p).data,
                'veiculos': VeiculoSerializer(p.veiculos.all(), many=True).data
            })

        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='quem-tem-mais')
    def quem_tem_mais(self, request):
        """
        Relatório: homens ou mulheres têm mais veículos.
        Endpoint: GET /api/veiculos/quem-tem-mais/
        """
        # values('sexo'): GROUP BY sexo
        # annotate(Count(...)): adiciona coluna calculada (COUNT)
        resultado = Pessoa.objects.values('sexo').annotate(
            total_veiculos=Count('veiculos')
        ).order_by('-total_veiculos')  # '-' inverte a ordem para DESC

        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='por-marca')
    def por_marca(self, request):
        """
        Relatório: todas as marcas ordenadas pelo número de veículos cadastrados.
        Endpoint: GET /api/veiculos/por-marca/
        """
        resultado = Veiculo.objects.values('marca').annotate(
            total=Count('id')
        ).order_by('-total')

        return Response(list(resultado))

    @action(detail=False, methods=['get'], url_path='marcas-por-sexo')
    def marcas_por_sexo(self, request):
        """
        Relatório: total de cada marca separado por sexo do proprietário.
        Endpoint: GET /api/veiculos/marcas-por-sexo/

        'proprietario__sexo': o __ atravessa a FK para acessar a tabela Pessoa
        """
        resultado = Veiculo.objects.values(
            'marca',
            'proprietario__sexo'
        ).annotate(
            total=Count('id')
        ).order_by('marca', '-total')

        return Response(list(resultado))


class RevisaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Revisao — gerencia o histórico de manutenções dos veículos.
    """
    
    # Declarado para o roteador (urls.py) gerar o basename da URL automaticamente
    queryset = Revisao.objects.all()
    serializer_class = RevisaoSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'oficina',                      # Busca na própria tabela de revisão
        'veiculo__placa',               # Vai na tabela veículo e busca a placa
        'veiculo__modelo',              # Vai na tabela veículo e busca o modelo
        'veiculo__proprietario__nome'   # Vai até a tabela pessoa e busca o nome do dono
    ]   

    def get_queryset(self):
        """
        Intercepta a busca no banco de dados para ordenar pela data e 
        permitir o filtro das revisões de um carro específico.
        Ex: /api/revisoes/?veiculo=10
        """
        # Pega todas as revisões, ordenadas da mais nova para a mais velha
        queryset = Revisao.objects.all().order_by('-data_revisao')
        
        # Tenta capturar o parâmetro '?veiculo=' enviado pelo Vue.js
        veiculo_id = self.request.query_params.get('veiculo', None)
        
        # Se existir, filtra retornando APENAS as revisões daquele carro
        if veiculo_id is not None:
            queryset = queryset.filter(veiculo_id=veiculo_id)
            
        return queryset

    @action(detail=False, methods=['get'], url_path='por-periodo')
    def por_periodo(self, request):
        """
        Relatório: revisões dentro de um período de datas.
        Endpoint: GET /api/revisoes/por-periodo/?inicio=2024-01-01&fim=2024-12-31
        """
        data_inicio = request.query_params.get('inicio')
        data_fim    = request.query_params.get('fim')

        revisoes = Revisao.objects.all()

        if data_inicio:
            revisoes = revisoes.filter(data_revisao__gte=data_inicio)
        if data_fim:
            revisoes = revisoes.filter(data_revisao__lte=data_fim)

        return Response(RevisaoSerializer(revisoes, many=True).data)

    @action(detail=False, methods=['get'], url_path='marcas-mais-revisoes')
    def marcas_mais_revisoes(self, request):
        """
        Relatório: marcas de veículos com maior número de revisões.
        Endpoint: GET /api/revisoes/marcas-mais-revisoes/
        """
        resultado = Revisao.objects.values(
            'veiculo__marca'
        ).annotate(
            total=Count('id')
        ).order_by('-total')

        return Response(list(resultado))

    @action(detail=False, methods=['get'], url_path='pessoas-mais-revisoes')
    def pessoas_mais_revisoes(self, request):
        """
        Relatório: pessoas (proprietários) com maior número de revisões.
        Endpoint: GET /api/revisoes/pessoas-mais-revisoes/
        """
        # Atravessa duas relações: revisão → veículo → proprietário → nome
        resultado = Revisao.objects.values(
            'veiculo__proprietario__nome'
        ).annotate(
            total=Count('id')
        ).order_by('-total')

        return Response(list(resultado))

    @action(detail=False, methods=['get'], url_path='media-tempo')
    def media_tempo(self, request):
        """
        Relatório: média de dias entre revisões por pessoa.
        Endpoint: GET /api/revisoes/media-tempo/

        Utiliza SQL puro com a Window Function (LAG) do PostgreSQL, 
        acessando o valor da linha anterior para calcular a diferença de dias.
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, AVG(diff) AS media_dias
                FROM (
                    SELECT
                        r.veiculo_id,
                        v.proprietario_id,
                        -- Calcula a diferença de dias entre esta revisão e a anterior
                        r.data_revisao - LAG(r.data_revisao) OVER (
                            PARTITION BY v.proprietario_id
                            ORDER BY r.data_revisao
                        ) AS diff
                    FROM alisson.revisoes r
                    JOIN alisson.veiculos v ON r.veiculo_id = v.id
                ) sub
                JOIN alisson.pessoas p ON sub.proprietario_id = p.id
                WHERE diff IS NOT NULL  -- descarta a primeira revisão (sem anterior)
                GROUP BY p.nome
                ORDER BY media_dias
            """)

            # Extrai os nomes das colunas e monta o dicionário
            colunas = [col[0] for col in cursor.description]
            resultado = [dict(zip(colunas, row)) for row in cursor.fetchall()]

        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='proximas-revisoes')
    def proximas_revisoes(self, request):
        """
        Relatório: próximas revisões previstas baseado no tempo médio histórico.
        Endpoint: GET /api/revisoes/proximas-revisoes/

        Soma a média de dias calculada com o LAG à data da última revisão 
        realizada para prever a próxima.
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    p.nome,
                    v.id AS veiculo_id,
                    v.marca,
                    v.modelo,
                    v.placa,
                    MAX(r.data_revisao) AS ultima_revisao,
                    AVG(diff)::integer AS media_dias,
                    MAX(r.data_revisao) + AVG(diff)::integer * INTERVAL '1 day' AS proxima_revisao
                FROM (
                    SELECT
                        r.id,
                        r.veiculo_id,
                        r.data_revisao,
                        r.data_revisao - LAG(r.data_revisao) OVER (
                            PARTITION BY r.veiculo_id
                            ORDER BY r.data_revisao
                        ) AS diff
                    FROM alisson.revisoes r
                ) r
                JOIN alisson.veiculos v ON r.veiculo_id = v.id
                JOIN alisson.pessoas p ON v.proprietario_id = p.id
                WHERE diff IS NOT NULL
                GROUP BY p.nome, v.id, v.marca, v.modelo, v.placa
                ORDER BY proxima_revisao
            """)

            colunas  = [col[0] for col in cursor.description]
            resultado = [dict(zip(colunas, row)) for row in cursor.fetchall()]

        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='revisoes-oficina')
    def revisoes_por_oficina(self, request):
        """
        Relatório: total de revisões realizadas separadas por oficina.
        Endpoint: GET /api/revisoes/revisoes-oficina/
        """
        # Agrupa pelo nome da oficina e conta quantos registros ('id') existem
        resultado = Revisao.objects.values('oficina').annotate(
            total=Count('id')
        ).order_by('-total')

        return Response(list(resultado))