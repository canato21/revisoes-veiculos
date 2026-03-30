"""
settings.py — Configuração central do Django
=============================================
Este é o arquivo mais importante do projeto no backend.
Todas as configurações do Django ficam aqui: banco de dados,
apps instalados, segurança, internacionalização, etc.
"""

from pathlib import Path
import os
from datetime import timedelta

# BASE_DIR aponta para a pasta raiz do backend (onde está o manage.py)
# Path(__file__) = caminho deste arquivo (settings.py)
# .resolve() = caminho absoluto
# .parent.parent = dois níveis acima (de core/ para backend/)
BASE_DIR = Path(__file__).resolve().parent.parent


# Segurança -------------

# Chave secreta usada para assinar cookies e tokens de segurança
SECRET_KEY = 'django-insecure-revisoes-veiculos-2024'

# DEBUG=True mostra erros detalhados no navegador
# Nesse caso está "true" para testes somente. Deixar "true" para um sistema em produção final expõe as informações internas do sistema 
DEBUG = True

# Lista de domínios que podem acessar o sistema
# '*' aceita qualquer domínio
ALLOWED_HOSTS = ['*']

# Aplicativos Instalados ----------
INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin', # painel administrativo em /admin
    'django.contrib.auth',  # sistema de usuários e autenticação
    'django.contrib.contenttypes', # sistema de tipos de conteúdo genérico
    'django.contrib.sessions', # gerenciamento de sessões de usuário
    'django.contrib.messages',  # sistema de mensagens flash
    'django.contrib.staticfiles', # servir arquivos estáticos (CSS, JS, imagens)

     # Pacotes de terceiros instalados via pip
    'rest_framework', # Django REST Framework — cria a API REST
    'corsheaders', # permite o Vue.js chamar a API de outro domínio
    'drf_spectacular', # gera documentação Swagger automaticamente em /api/docs/
    'rest_framework_simplejwt', # autenticação por tokens JWT

    # Nosso app principal com models, views, serializers, etc.
    'veiculos',
]

# ── MIDDLEWARE ────────────────────────────────────────────────────────────────
# Middleware são "interceptadores" que processam cada requisição antes de
# chegar na view e cada resposta antes de sair. Funcionam como camadas.
# A requisição passa pela ordem de cima para baixo, a resposta de baixo para cima.

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # DEVE ser o primeiro — adiciona headers CORS
    'django.middleware.security.SecurityMiddleware', # headers de segurança HTTP
    'django.contrib.sessions.middleware.SessionMiddleware', # gerencia sessões
    'django.middleware.common.CommonMiddleware',  # normaliza URLs
    'django.middleware.csrf.CsrfViewMiddleware', # proteção contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # identifica o usuário
    'django.contrib.messages.middleware.MessageMiddleware',  # mensagens flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # proteção clickjacking
]

# arquivo que define todas as URLs do projeto
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ── BANCO DE DADOS ────────────────────────────────────────────────────────────
# Usamos os.environ.get(CHAVE, VALOR_PADRAO) para que o mesmo código
# funcione tanto dentro do Docker (usa variáveis de ambiente) quanto
# rodando direto no WSL (usa os valores padrão).
#
# Dentro do Docker:  HOST=db      PORT=5432  (rede interna Docker)
# Fora do Docker:    HOST=localhost PORT=5433 (porta mapeada para o PC)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # driver do PostgreSQL
        'NAME': os.environ.get('DJANGO_DB_NAME', 'revisoes'),
        'USER': os.environ.get('DJANGO_DB_USER', 'alisson'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'senha123'),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DB_PORT', '5433'),
    }
}

LANGUAGE_CODE = 'pt-br' # idioma padrão
TIME_ZONE = 'America/Sao_Paulo' # fuso horário do Brasil
USE_I18N = True # habilita internacionalização
USE_TZ = True # habilita internacionalização

# Arquivos Estáticos ----
STATIC_URL = 'static/' # URL pública dos arquivos estáticos

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

# CORS -------------
# CORS (Cross-Origin Resource Sharing) permite que o Vue.js (localhost:5173)
# faça requisições para o Django (localhost:8000) sem ser bloqueado pelo navegador.
# True = aceita requisições de qualquer origem (OK para desenvolvimento)
CORS_ALLOW_ALL_ORIGINS = True

# DJANGO REST FRAMEWORK -----------
REST_FRAMEWORK = {
    # Todo endpoint da API exige que o usuário esteja autenticado
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
     # A autenticação é feita via token JWT no header Authorization: Bearer <token>
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Classe que gera o schema OpenAPI para o Swaggers
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# JWT (JSON WEB TOKEN)-------------
# Configurações dos tokens de autenticação.
# ACCESS TOKEN: token de curta duração usado nas requisições da API
# REFRESH TOKEN: token de longa duração usado para gerar novos access tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}