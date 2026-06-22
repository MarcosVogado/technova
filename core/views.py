from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from .models import Cliente, Produto, Venda
from .serializers import ClienteSerializer, ProdutoSerializer, VendaSerializer, VendaCreateSerializer
from .services import VendaService
from .exceptions import ClienteComVendasError


# ============================================================
#  API REST
# ============================================================

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """Impede exclusão de cliente com vendas registradas (regra de negócio)."""
        cliente = self.get_object()
        if cliente.vendas.exists():
            raise ClienteComVendasError()
        return super().destroy(request, *args, **kwargs)


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.prefetch_related('itens', 'itens__produto').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return VendaCreateSerializer
        return VendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = VendaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cliente = get_object_or_404(Cliente, id=serializer.validated_data['cliente'])

        venda = VendaService.registrar_venda(
            cliente=cliente,
            usuario=request.user,
            itens_data=serializer.validated_data['itens'],
            observacoes=serializer.validated_data.get('observacoes', '')
        )
        return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)


@extend_schema(
    responses=OpenApiTypes.OBJECT,
    description='Resumo consolidado de vendas (total de vendas e valor acumulado) + lista de vendas.',
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def relatorio_vendas(request):
    qs = Venda.objects.all()
    resumo = qs.aggregate(total_vendas=Count('id'), valor_total=Sum('valor_total'))
    return Response({
        'resumo': {
            'total_vendas': resumo['total_vendas'] or 0,
            'valor_total': str(resumo['valor_total'] or 0),
        },
        'vendas': VendaSerializer(qs, many=True).data
    })


# ============================================================
#  Interface Web — apenas renderiza os templates (shells).
#  Todo o carregamento/escrita de dados é feito via fetch na API REST.
# ============================================================

def login_web(request):
    return render(request, 'core/login.html')


def home_web(request):
    return render(request, 'core/home.html')


def listar_produtos(request):
    return render(request, 'core/produtos.html')


def clientes_web(request):
    return render(request, 'core/clientes.html')


def nova_venda_web(request):
    return render(request, 'core/nova_venda.html')


def lista_vendas_web(request):
    return render(request, 'core/lista_vendas.html')
