from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cliente, Produto, Venda
from .services import VendaService

class TechNovaTests(TestCase):
    def setUp(self):
        # Criar usuário para autenticação
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Criar dados iniciais
        self.cliente = Cliente.objects.create(
            nome="João Teste", 
            cpf="123.456.789-00", 
            email="joao@teste.com"
        )
        self.produto = Produto.objects.create(
            nome="Teclado Mecânico", 
            preco=Decimal("250.00"), 
            quantidade_estoque=10,
            estoque_minimo=2
        )

    def test_registrar_venda_sucesso(self):
        """Testa se a venda é registrada e o estoque é baixado"""
        # AQUI: Mudado de 'produto' para 'produto_id' para bater com seu services.py
        itens_data = [{'produto_id': self.produto.id, 'quantidade': 2}]
        venda = VendaService.registrar_venda(
            cliente=self.cliente,
            usuario=self.user,
            itens_data=itens_data
        )
        
        self.produto.refresh_from_db()
        self.assertEqual(venda.valor_total, Decimal("500.00"))
        self.assertEqual(self.produto.quantidade_estoque, 8)

    def test_venda_estoque_insuficiente(self):
        """Testa se o sistema impede venda acima do estoque disponível"""
        itens_data = [{'produto_id': self.produto.id, 'quantidade': 99}]
        
        from .exceptions import EstoqueInsuficienteError
        with self.assertRaises(EstoqueInsuficienteError):
            VendaService.registrar_venda(
                cliente=self.cliente,
                usuario=self.user,
                itens_data=itens_data
            )

    def test_api_lista_clientes(self):
        """Testa se o endpoint da API está respondendo"""
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exclusao_cliente_com_venda_protegida(self):
        """Testa se o models.PROTECT está funcionando via API"""
        VendaService.registrar_venda(
            cliente=self.cliente,
            usuario=self.user,
            itens_data=[{'produto_id': self.produto.id, 'quantidade': 1}]
        )
        
        # A API deve retornar 400 porque a ViewSet chama o erro customizado
        response = self.client.delete(f'/api/clientes/{self.cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)