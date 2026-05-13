from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'produtos', views.ProdutoViewSet)
router.register(r'vendas', views.VendaViewSet)

urlpatterns = [
    
    path('api/', include(router.urls)),
    path('api/relatorio/', views.relatorio_vendas, name='api_relatorio'),

    
    path('', views.home_web, name='home'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('vendas/nova/', views.nova_venda_web, name='nova_venda'),
    path('vendas/historico/', views.lista_vendas_web, name='lista_vendas'),
]