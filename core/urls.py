from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'vendas', views.VendaViewSet)

urlpatterns = [
    # --- API REST (protegida por JWT) ---
    path('api/', include(router.urls)),
    path('api/relatorios/vendas/', views.relatorio_vendas, name='relatorio_vendas'),

    # --- Interface Web (shells que consomem a API via fetch) ---
    path('login/', views.login_web, name='login'),
    path('', views.home_web, name='home'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('clientes/', views.clientes_web, name='clientes'),
    path('vendas/nova/', views.nova_venda_web, name='nova_venda'),
    path('vendas/historico/', views.lista_vendas_web, name='lista_vendas'),
]
