from django.contrib import admin
from .models import Cliente, Produto, Venda, ItemVenda


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 0

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email')
    search_fields = ('nome', 'cpf')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade_estoque')
    list_filter = ('preco',)

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_venda', 'valor_total')
    inlines = [ItemVendaInline] 