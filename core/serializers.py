from rest_framework import serializers
from .models import Cliente, Produto, Venda, ItemVenda

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ItemVendaSerializer(serializers.ModelSerializer):
    # Mostra o nome do produto ao invés de só o ID
    produto_nome = serializers.ReadOnlyField(source='produto.nome')

    class Meta:
        model = ItemVenda
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario']

class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    cliente_nome = serializers.ReadOnlyField(source='cliente.nome')

    class Meta:
        model = Venda
        fields = ['id', 'cliente', 'cliente_nome', 'data_venda', 'total', 'itens']