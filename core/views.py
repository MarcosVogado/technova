from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F, Sum, Count
from .models import Cliente, Produto, Venda
from .serializers import ClienteSerializer, ProdutoSerializer, VendaSerializer, VendaCreateSerializer
from .services import VendaService
from .exceptions import ClienteComVendasError



class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """Impede exclusão de cliente com vendas (Regra do Marcos)"""
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



def home_web(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_produtos': Produto.objects.count(),
        'produtos_alerta': Produto.objects.filter(quantidade_estoque__lte=F('estoque_minimo')),
    }
    return render(request, 'core/home.html', context)

def listar_produtos(request):
    return render(request, 'core/produtos.html', {'produtos': Produto.objects.all()})

def lista_vendas_web(request):
    """Nova tela de histórico solicitada"""
    vendas = Venda.objects.all().order_by('-data_venda')
    return render(request, 'core/lista_vendas.html', {'vendas': vendas})

def nova_venda_web(request):
    if request.method == "POST":
        try:
            cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
            VendaService.registrar_venda(
                cliente=cliente,
                usuario=request.user,
                itens_data=[{
                    'produto': int(request.POST.get('produto')), 
                    'quantidade': int(request.POST.get('quantidade'))
                }]
            )
            messages.success(request, "TRANSACAO_AUTORIZADA: Sistema atualizado.")
            return redirect('lista_vendas') # Redireciona para o histórico após vender
        except Exception as e:
            messages.error(request, f"FALHA_CRITICA: {str(e)}")
    
    context = {
        'clientes': Cliente.objects.all(),
        'produtos': Produto.objects.filter(quantidade_estoque__gt=0)
    }
    return render(request, 'core/nova_venda.html', context)