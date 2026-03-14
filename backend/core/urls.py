from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from veiculos.views import PessoaViewSet, VeiculoViewSet, RevisaoViewSet

router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'revisoes', RevisaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]