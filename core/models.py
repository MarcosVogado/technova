from django.db import models
from django.core.exceptions import ValidationError

class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF") 
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)

    def clean(self):
        if self.estoque < 0:
            raise ValidationError("O estoque não pode ser negativo.")
        if self.preco < 0:
            raise ValidationError("O preço não pode ser negativo.")

    def __str__(self):
        return self.nome

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"