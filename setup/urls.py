from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# AQUI ESTÁ O SEGREDO: Importando tudo certinho do seu core/views.py
from core.views import (
    ClienteViewSet,
    ProdutoViewSet,
    VendaViewSet,
    relatorio_vendas,  # <--- Essa aqui costuma causar o erro se esquecer
    home_web,
    listar_produtos,
    nova_venda_web
)

# Configuração do Roteador para a API
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)

urlpatterns = [
    # Painel Administrativo
    path('admin/', admin.site.urls),

    # --- NAVEGAÇÃO WEB (Interface Futurista TechNova) ---
    path('', home_web, name='home'),
    path('produtos/', listar_produtos, name='listar_produtos'),
    path('venda/nova/', nova_venda_web, name='nova_venda'),

    # --- API REST (Rotas Automáticas) ---
    path('api/', include(router.urls)),

    # --- AUTENTICAÇÃO JWT (Padrão exigido pelo Marcos) ---
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # --- RELATÓRIOS (Nova rota exigida) ---
    path('api/relatorios/vendas/', relatorio_vendas, name='relatorio_vendas'),
]