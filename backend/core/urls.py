"""
urls.py — Mapa de rotas da API
==============================
Este arquivo define todas as URLs disponíveis no backend.
O Django lê este arquivo e sabe para qual função/classe enviar
cada requisição recebida.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from veiculos.views import PessoaViewSet, VeiculoViewSet, RevisaoViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ── ROUTER ────────────────────────────────────────────────────────────────────
# O DefaultRouter gera automaticamente todas as rotas CRUD para cada ViewSet.
# Para cada registro (ex: 'pessoas'), ele cria:
#   GET    /api/pessoas/        - lista todos
#   POST   /api/pessoas/        - cria um novo
#   GET    /api/pessoas/{id}/   - busca um pelo ID
#   PUT    /api/pessoas/{id}/   - atualiza um pelo ID
#   DELETE /api/pessoas/{id}/   - deleta um pelo ID
# Além das rotas @action customizadas definidas nas views

router = DefaultRouter()
router.register(r'pessoas',  PessoaViewSet) # prefixo da URL = 'pessoas'
router.register(r'veiculos', VeiculoViewSet) # prefixo da URL = 'veiculos'
router.register(r'revisoes', RevisaoViewSet) # prefixo da URL = 'revisoes'

# URL -------------
urlpatterns = [
    # Painel administrativo do Django — interface visual para gerenciar dados
    path('admin/', admin.site.urls),

    # Todas as rotas da API registradas no router acima
    # include() importa todas as rotas geradas pelo router de uma vez
    path('api/', include(router.urls)),

    # Autenticação JWT — recebe usuário e senha, retorna access + refresh token
    # POST /api/token/ com body: { "username": "alisson", "password": "senha123" }
    # Retorna: { "access": "eyJ...", "refresh": "eyJ..." }
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Renovação de token — recebe o refresh token, retorna novo access token
    # POST /api/token/refresh/ com body: { "refresh": "eyJ..." }
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

     # Schema OpenAPI — retorna o JSON com toda a documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Interface visual Swagger — documentação interativa em /api/docs/
    # Permite testar os endpoints diretamente pelo navegador
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]