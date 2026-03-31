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
from django.core.cache import cache
from datetime import date

from .models import Pessoa, Veiculo, Revisao
from .serializers import PessoaSerializer, VeiculoSerializer, RevisaoSerializer

# Tempo padrão de duração do cache (15 minutos = 900 segundos)
TEMPO_CACHE = 900 

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all().order_by('nome')
    serializer_class = PessoaSerializer 
    filter_backends = [SearchFilter]
    search_fields = ['nome', 'cpf', 'email', 'telefone']

    # ── LIMPEZA DE CACHE ──
    def limpar_caches_pessoa(self):
        chaves_fixas = [
            'dashboard_resumo', # Atualiza contadores do dashboard
            'pessoas_por_sexo', 'veiculos_por_pessoa', 'veiculos_quem_tem_mais', 
            'veiculos_marcas_sexo', 'revisoes_pessoas_mais', 'revisoes_media_tempo', 'revisoes_proximas'
        ]
        for chave in chaves_fixas:
            cache.delete(chave)
        
        # Limpa todas as chaves dinâmicas de filtro de idade geradas pelo Redis
        chaves_idade = cache.keys("pessoas_idade_*")
        if chaves_idade:
            cache.delete_many(chaves_idade)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.limpar_caches_pessoa()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.limpar_caches_pessoa()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.limpar_caches_pessoa()

    # ── RELATÓRIOS (Com Cache) ──
    @action(detail=False, methods=['get'], url_path='por-sexo')
    def por_sexo(self, request):
        dados_cacheados = cache.get('pessoas_por_sexo')
        if dados_cacheados:
            return Response(dados_cacheados)

        pessoas = Pessoa.objects.all()
        resultado = { 'masculino': [], 'feminino': [], 'idade_media_m': 0, 'idade_media_f': 0 }
        idades_m, idades_f = [], []
        hoje = date.today()

        for p in pessoas:
            idade = hoje.year - p.data_nascimento.year
            dados = PessoaSerializer(p).data
            dados['idade'] = idade 

            if p.sexo == 'M':
                resultado['masculino'].append(dados)
                idades_m.append(idade)
            else:
                resultado['feminino'].append(dados)
                idades_f.append(idade)

        resultado['idade_media_m'] = round(sum(idades_m) / len(idades_m), 1) if idades_m else 0
        resultado['idade_media_f'] = round(sum(idades_f) / len(idades_f), 1) if idades_f else 0

        cache.set('pessoas_por_sexo', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='idade')
    def por_idade(self, request):
        data_comeco = request.query_params.get('inicio', 'todos')
        data_final = request.query_params.get('fim', 'todos')
        
        # CHAVE DINÂMICA
        chave_dinamica = f"pessoas_idade_{data_comeco}_{data_final}"
        dados_cacheados = cache.get(chave_dinamica)
        if dados_cacheados:
            return Response(dados_cacheados)

        pessoas = Pessoa.objects.all()
        if data_comeco != 'todos':
            pessoas = pessoas.filter(data_nascimento__gte=data_comeco)
        if data_final != 'todos':
            pessoas = pessoas.filter(data_nascimento__lte=data_final)

        dados_finais = PessoaSerializer(pessoas, many=True).data
        cache.set(chave_dinamica, dados_finais, timeout=TEMPO_CACHE)
        return Response(dados_finais)


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all().select_related('proprietario').order_by('id')
    serializer_class = VeiculoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['marca', 'modelo', 'placa', 'proprietario__nome']

    # ── LIMPEZA DE CACHE ──
    def limpar_caches_veiculo(self):
        chaves = [
            'dashboard_resumo', # Atualiza contadores do dashboard
            'veiculos_por_pessoa', 'veiculos_quem_tem_mais', 'veiculos_por_marca', 
            'veiculos_marcas_sexo', 'revisoes_marcas_mais', 'revisoes_proximas'
        ]
        for chave in chaves:
            cache.delete(chave)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.limpar_caches_veiculo()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.limpar_caches_veiculo()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.limpar_caches_veiculo()

    def get_queryset(self):
        queryset = Veiculo.objects.all().select_related('proprietario')
        proprietario_id = self.request.query_params.get('proprietario')
        if proprietario_id:
            queryset = queryset.filter(proprietario_id=proprietario_id)
        return queryset

    # ── RELATÓRIOS (Com Cache) ──
    @action(detail=False, methods=['get'], url_path='por-pessoa')
    def por_pessoa(self, request):
        dados_cacheados = cache.get('veiculos_por_pessoa')
        if dados_cacheados: return Response(dados_cacheados)

        pessoas = Pessoa.objects.prefetch_related('veiculos').order_by('nome')
        resultado = []
        for p in pessoas:
            resultado.append({
                'pessoa': PessoaSerializer(p).data,
                'veiculos': VeiculoSerializer(p.veiculos.all(), many=True).data
            })
            
        cache.set('veiculos_por_pessoa', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='quem-tem-mais')
    def quem_tem_mais(self, request):
        dados_cacheados = cache.get('veiculos_quem_tem_mais')
        if dados_cacheados: return Response(dados_cacheados)

        resultado = list(Pessoa.objects.values('sexo').annotate(total_veiculos=Count('veiculos')).order_by('-total_veiculos'))
        cache.set('veiculos_quem_tem_mais', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='por-marca')
    def por_marca(self, request):
        dados_cacheados = cache.get('veiculos_por_marca')
        if dados_cacheados: return Response(dados_cacheados)

        resultado = list(Veiculo.objects.values('marca').annotate(total=Count('id')).order_by('-total'))
        cache.set('veiculos_por_marca', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='marcas-por-sexo')
    def marcas_por_sexo(self, request):
        dados_cacheados = cache.get('veiculos_marcas_sexo')
        if dados_cacheados: return Response(dados_cacheados)

        resultado = list(Veiculo.objects.values('marca', 'proprietario__sexo').annotate(total=Count('id')).order_by('marca', '-total'))
        cache.set('veiculos_marcas_sexo', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)
    
    @action(detail=False, methods=['get'], url_path='resumo')
    def resumo_totais(self, request):
        dados_cacheados = cache.get('dashboard_resumo')
        if dados_cacheados: return Response(dados_cacheados)

        dados = {
            'pessoas': Pessoa.objects.count(),
            'veiculos': Veiculo.objects.count(),
            'revisoes': Revisao.objects.count()
        }
        
        cache.set('dashboard_resumo', dados, timeout=TEMPO_CACHE)
        return Response(dados)


class RevisaoViewSet(viewsets.ModelViewSet):
    queryset = Revisao.objects.all()
    serializer_class = RevisaoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['oficina', 'veiculo__placa', 'veiculo__modelo', 'veiculo__proprietario__nome']

    # ── LIMPEZA DE CACHE ──
    def limpar_caches_revisao(self):
        chaves = [
            'dashboard_resumo', # Atualiza contadores do dashboard
            'revisoes_marcas_mais', 'revisoes_pessoas_mais', 
            'revisoes_media_tempo', 'revisoes_proximas', 'revisoes_oficina'
        ]
        for chave in chaves:
            cache.delete(chave)
            
        # Limpa todas as chaves dinâmicas de filtro por data geradas pelo Redis
        chaves_periodo = cache.keys("revisoes_periodo_*")
        if chaves_periodo:
            cache.delete_many(chaves_periodo)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.limpar_caches_revisao()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.limpar_caches_revisao()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.limpar_caches_revisao()

    def get_queryset(self):
        queryset = Revisao.objects.all().order_by('-data_revisao')
        veiculo_id = self.request.query_params.get('veiculo', None)
        if veiculo_id is not None:
            queryset = queryset.filter(veiculo_id=veiculo_id)
        return queryset

    # ── RELATÓRIOS (Com Cache) ──
    @action(detail=False, methods=['get'], url_path='por-periodo')
    def por_periodo(self, request):
        data_inicio = request.query_params.get('inicio', 'todos')
        data_fim    = request.query_params.get('fim', 'todos')
        
        # CHAVE DINÂMICA
        chave_dinamica = f"revisoes_periodo_{data_inicio}_{data_fim}"
        dados_cacheados = cache.get(chave_dinamica)
        if dados_cacheados:
            return Response(dados_cacheados)

        revisoes = Revisao.objects.all()
        if data_inicio != 'todos': 
            revisoes = revisoes.filter(data_revisao__gte=data_inicio)
        if data_fim != 'todos':    
            revisoes = revisoes.filter(data_revisao__lte=data_fim)

        dados_finais = RevisaoSerializer(revisoes, many=True).data
        cache.set(chave_dinamica, dados_finais, timeout=TEMPO_CACHE)
        return Response(dados_finais)

    @action(detail=False, methods=['get'], url_path='marcas-mais-revisoes')
    def marcas_mais_revisoes(self, request):
        dados_cacheados = cache.get('revisoes_marcas_mais')
        if dados_cacheados: return Response(dados_cacheados)

        resultado = list(Revisao.objects.values('veiculo__marca').annotate(total=Count('id')).order_by('-total'))
        cache.set('revisoes_marcas_mais', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='pessoas-mais-revisoes')
    def pessoas_mais_revisoes(self, request):
        dados_cacheados = cache.get('revisoes_pessoas_mais')
        if dados_cacheados: return Response(dados_cacheados)

        resultado = list(Revisao.objects.values('veiculo__proprietario__nome').annotate(total=Count('id')).order_by('-total'))
        cache.set('revisoes_pessoas_mais', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='media-tempo')
    def media_tempo(self, request):
        dados_cacheados = cache.get('revisoes_media_tempo')
        if dados_cacheados: return Response(dados_cacheados)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, AVG(diff) AS media_dias
                FROM (
                    SELECT 
                        r.veiculo_id, v.proprietario_id,
                        r.data_revisao - LAG(r.data_revisao) OVER (
                            PARTITION BY v.proprietario_id ORDER BY r.data_revisao
                        ) AS diff
                    FROM alisson.revisoes r
                    JOIN alisson.veiculos v ON r.veiculo_id = v.id
                ) sub
                JOIN alisson.pessoas p ON sub.proprietario_id = p.id
                WHERE diff IS NOT NULL
                GROUP BY p.nome
                ORDER BY media_dias
            """)
            colunas = [col[0] for col in cursor.description]
            resultado = [dict(zip(colunas, row)) for row in cursor.fetchall()]

        cache.set('revisoes_media_tempo', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='proximas-revisoes')
    def proximas_revisoes(self, request):
        dados_cacheados = cache.get('revisoes_proximas')
        if dados_cacheados: return Response(dados_cacheados)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.nome, v.id AS veiculo_id, v.marca, v.modelo, v.placa,
                    MAX(r.data_revisao) AS ultima_revisao,
                    AVG(diff)::integer AS media_dias,
                    MAX(r.data_revisao) + AVG(diff)::integer * INTERVAL '1 day' AS proxima_revisao
                FROM (
                    SELECT 
                        r.id, r.veiculo_id, r.data_revisao,
                        r.data_revisao - LAG(r.data_revisao) OVER (
                            PARTITION BY r.veiculo_id ORDER BY r.data_revisao
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

        cache.set('revisoes_proximas', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='revisoes-oficina')
    def revisoes_por_oficina(self, request):
        dados_cacheados = cache.get('revisoes_oficina')
        if dados_cacheados: return Response(dados_cacheados)

        resultado = list(Revisao.objects.values('oficina').annotate(total=Count('id')).order_by('-total'))
        cache.set('revisoes_oficina', resultado, timeout=TEMPO_CACHE)
        return Response(resultado)