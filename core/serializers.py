import re
from rest_framework import serializers
from .models import Cliente, Produto, Venda, ItemVenda

# --- CLIENTE ---
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_cpf(self, value):
        cpf_limpo = re.sub(r'\D', '', value)
        if len(cpf_limpo) != 11:
            raise serializers.ValidationError('CPF deve conter 11 dígitos.')
        return value

# --- PRODUTO ---
class ProdutoSerializer(serializers.ModelSerializer):
    estoque_baixo = serializers.ReadOnlyField()

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'categoria', 'preco',
            'quantidade_estoque', 'estoque_minimo', 'ativo',
            'estoque_baixo',
        ]

# --- ITENS DA VENDA ---
class ItemVendaSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')

    class Meta:
        model = ItemVenda
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario', 'subtotal']
        read_only_fields = ['preco_unitario', 'subtotal']

class ItemVendaWriteSerializer(serializers.Serializer):
    """Auxiliar para o processo de escrita"""
    produto = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1)

# --- VENDA (LEITURA) ---
class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    cliente_nome = serializers.ReadOnlyField(source='cliente.nome')
    usuario_nome = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Venda
        fields = [
            'id', 'data_venda', 'cliente', 'cliente_nome',
            'usuario', 'usuario_nome', 'valor_total',
            'observacoes', 'itens',
        ]
        read_only_fields = ['valor_total', 'usuario']

# --- VENDA (ESCRITA - O QUE ESTAVA FALTANDO!) ---
class VendaCreateSerializer(serializers.Serializer):
    cliente = serializers.IntegerField()
    observacoes = serializers.CharField(required=False, allow_blank=True, default='')
    itens = ItemVendaWriteSerializer(many=True)

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError('A venda deve conter pelo menos um item.')
        return value