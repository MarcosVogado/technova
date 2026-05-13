from decimal import Decimal
from django.db import transaction
from .models import Produto, Venda, ItemVenda
from .exceptions import EstoqueInsuficienteError

class VendaService:
    @staticmethod
    @transaction.atomic
    def registrar_venda(cliente, usuario, itens_data, observacoes=''):
        """Lógica central exigida na Entrega 2"""
        # 1. Validar estoque
        produtos_confirmados = []
        for item in itens_data:
            produto = Produto.objects.select_for_update().get(id=item['produto_id'])
            if produto.quantidade_estoque < item['quantidade']:
                raise EstoqueInsuficienteError(detail=f"Estoque insuficiente: {produto.nome}")
            produtos_confirmados.append((produto, item['quantidade']))

        # 2. Criar a venda
        venda = Venda.objects.create(cliente=cliente, usuario=usuario, observacoes=observacoes)

        # 3. Baixar estoque e criar itens
        total = Decimal('0.00')
        for produto, qtd in produtos_confirmados:
            subtotal = produto.preco * qtd
            ItemVenda.objects.create(
                venda=venda, produto=produto, quantidade=qtd,
                preco_unitario=produto.preco, subtotal=subtotal
            )
            produto.quantidade_estoque -= qtd
            produto.save()
            total += subtotal

        venda.valor_total = total
        venda.save()
        return venda