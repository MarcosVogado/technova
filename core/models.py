from django.db import models
from django.conf import settings


class Cliente(models.Model):
    nome     = models.CharField(max_length=150)
    cpf      = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    email    = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome            = models.CharField(max_length=200)
    descricao       = models.TextField(blank=True, null=True, verbose_name="Descrição")
    categoria       = models.CharField(max_length=50, blank=True, null=True)
    preco           = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField(default=0, verbose_name="Estoque")
    estoque_minimo  = models.IntegerField(default=5)
    ativo           = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo


class Venda(models.Model):
    data_venda  = models.DateTimeField(auto_now_add=True)
    cliente     = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,   
        related_name='vendas'
    )
    usuario     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='vendas'
    )
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        ordering = ['-data_venda']

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.nome}"


class ItemVenda(models.Model):
    venda          = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
        related_name='itens'
    )
    produto        = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='itens_venda'
    )
    quantidade     = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal       = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"