from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import (
    ClienteViewSet,
    ProdutoViewSet,
    VendaViewSet,
    relatorio_vendas,  
    home_web,
    listar_produtos,
    nova_venda_web,
    lista_vendas_web
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home_web, name='home'),
    path('produtos/', listar_produtos, name='listar_produtos'),
    path('venda/nova/', nova_venda_web, name='nova_venda'),
    path('vendas/historico/', lista_vendas_web, name='lista_vendas'),

    path('api/', include(router.urls)),

    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/relatorios/vendas/', relatorio_vendas, name='relatorio_vendas'),
]