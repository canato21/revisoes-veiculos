from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.db import connection
from .models import Pessoa, Veiculo, Revisao
from .serializers import PessoaSerializer, VeiculoSerializer, RevisaoSerializer


class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all().order_by('nome')
    serializer_class = PessoaSerializer

    @action(detail=False, methods=['get'], url_path='por-sexo')
    def por_sexo(self, request):
        """Pessoas separadas por sexo com idade média"""
        from datetime import date
        pessoas = Pessoa.objects.all()
        resultado = {'masculino': [], 'feminino': [], 'idade_media_m': 0, 'idade_media_f': 0}
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
        return Response(resultado)


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all().select_related('proprietario')
    serializer_class = VeiculoSerializer

    @action(detail=False, methods=['get'], url_path='por-pessoa')
    def por_pessoa(self, request):
        """Veículos agrupados por pessoa ordenado por nome"""
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
        """Homens ou mulheres têm mais veículos"""
        resultado = Pessoa.objects.values('sexo').annotate(
            total_veiculos=Count('veiculos')
        ).order_by('-total_veiculos')
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='por-marca')
    def por_marca(self, request):
        """Marcas ordenadas pelo número de veículos"""
        resultado = Veiculo.objects.values('marca').annotate(
            total=Count('id')
        ).order_by('-total')
        return Response(list(resultado))

    @action(detail=False, methods=['get'], url_path='marcas-por-sexo')
    def marcas_por_sexo(self, request):
        """Totais de marcas separados entre homens e mulheres"""
        resultado = Veiculo.objects.values(
            'marca', 'proprietario__sexo'
        ).annotate(total=Count('id')).order_by('marca', '-total')
        return Response(list(resultado))


class RevisaoViewSet(viewsets.ModelViewSet):
    queryset = Revisao.objects.all().select_related('veiculo__proprietario')
    serializer_class = RevisaoSerializer

    @action(detail=False, methods=['get'], url_path='por-periodo')
    def por_periodo(self, request):
        """Revisões dentro de um período"""
        data_inicio = request.query_params.get('inicio')
        data_fim = request.query_params.get('fim')
        revisoes = Revisao.objects.all()
        if data_inicio:
            revisoes = revisoes.filter(data_revisao__gte=data_inicio)
        if data_fim:
            revisoes = revisoes.filter(data_revisao__lte=data_fim)
        return Response(RevisaoSerializer(revisoes, many=True).data)

    @action(detail=False, methods=['get'], url_path='marcas-mais-revisoes')
    def marcas_mais_revisoes(self, request):
        """Marcas com maior número de revisões"""
        resultado = Revisao.objects.values(
            'veiculo__marca'
        ).annotate(total=Count('id')).order_by('-total')
        return Response(list(resultado))

    @action(detail=False, methods=['get'], url_path='pessoas-mais-revisoes')
    def pessoas_mais_revisoes(self, request):
        """Pessoas com maior número de revisões"""
        resultado = Revisao.objects.values(
            'veiculo__proprietario__nome'
        ).annotate(total=Count('id')).order_by('-total')
        return Response(list(resultado))

    @action(detail=False, methods=['get'], url_path='media-tempo')
    def media_tempo(self, request):
        """Média de tempo entre revisões por pessoa"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, AVG(diff) as media_dias
                FROM (
                    SELECT r.veiculo_id,
                           v.proprietario_id,
                           r.data_revisao - LAG(r.data_revisao) OVER (
                               PARTITION BY v.proprietario_id ORDER BY r.data_revisao
                           ) as diff
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
        return Response(resultado)

    @action(detail=False, methods=['get'], url_path='proximas-revisoes')
    def proximas_revisoes(self, request):
        """Próximas revisões baseado no tempo médio"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, v.marca, v.modelo, v.placa,
                       MAX(r.data_revisao) as ultima_revisao,
                       AVG(diff)::integer as media_dias,
                       MAX(r.data_revisao) + AVG(diff)::integer * INTERVAL '1 day' as proxima_revisao
                FROM (
                    SELECT r.id, r.veiculo_id, r.data_revisao,
                           r.data_revisao - LAG(r.data_revisao) OVER (
                               PARTITION BY r.veiculo_id ORDER BY r.data_revisao
                           ) as diff
                    FROM alisson.revisoes r
                ) r
                JOIN alisson.veiculos v ON r.veiculo_id = v.id
                JOIN alisson.pessoas p ON v.proprietario_id = p.id
                WHERE diff IS NOT NULL
                GROUP BY p.nome, v.marca, v.modelo, v.placa
                ORDER BY proxima_revisao
            """)
            colunas = [col[0] for col in cursor.description]
            resultado = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        return Response(resultado)