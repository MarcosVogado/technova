from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cliente, Produto
from .services import VendaService
from .exceptions import EstoqueInsuficienteError


class TechNovaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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

    # ---------- Regras de negócio (Service Layer) ----------

    def test_registrar_venda_sucesso(self):
        """A venda é registrada e o estoque é baixado corretamente."""
        itens_data = [{'produto_id': self.produto.id, 'quantidade': 2}]
        venda = VendaService.registrar_venda(
            cliente=self.cliente, usuario=self.user, itens_data=itens_data
        )
        self.produto.refresh_from_db()
        self.assertEqual(venda.valor_total, Decimal("500.00"))
        self.assertEqual(self.produto.quantidade_estoque, 8)

    def test_venda_estoque_insuficiente(self):
        """O sistema impede venda acima do estoque disponível."""
        itens_data = [{'produto_id': self.produto.id, 'quantidade': 99}]
        with self.assertRaises(EstoqueInsuficienteError):
            VendaService.registrar_venda(
                cliente=self.cliente, usuario=self.user, itens_data=itens_data
            )

    # ---------- API REST ----------

    def test_api_lista_clientes(self):
        """O endpoint da API responde para usuário autenticado."""
        response = self.client.get('/api/clientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exclusao_cliente_com_venda_protegida(self):
        """models.PROTECT + regra de negócio bloqueiam exclusão de cliente com vendas."""
        VendaService.registrar_venda(
            cliente=self.cliente, usuario=self.user,
            itens_data=[{'produto_id': self.produto.id, 'quantidade': 1}]
        )
        response = self.client.delete(f'/api/clientes/{self.cliente.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_produto_via_api(self):
        """CRUD: criação de produto via API."""
        payload = {
            'nome': 'Mouse Gamer', 'preco': '120.00',
            'quantidade_estoque': 15, 'estoque_minimo': 3, 'ativo': True
        }
        response = self.client.post('/api/produtos/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Produto.objects.filter(nome='Mouse Gamer').exists())

    def test_produto_preco_invalido(self):
        """Validação: preço deve ser maior que zero."""
        response = self.client.post('/api/produtos/', {
            'nome': 'Produto Zero', 'preco': '0', 'quantidade_estoque': 1
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cpf_invalido(self):
        """Validação: CPF deve conter 11 dígitos."""
        response = self.client.post('/api/clientes/', {
            'nome': 'Maria', 'cpf': '123', 'email': 'maria@teste.com'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_venda_via_api_multi_itens(self):
        """Venda com múltiplos itens via API baixa o estoque corretamente."""
        outro = Produto.objects.create(nome="Monitor", preco=Decimal("900.00"), quantidade_estoque=5)
        payload = {
            'cliente': self.cliente.id,
            'itens': [
                {'produto': self.produto.id, 'quantidade': 2},
                {'produto': outro.id, 'quantidade': 1},
            ]
        }
        response = self.client.post('/api/vendas/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['valor_total']), Decimal("1400.00"))


class JWTAuthTests(TestCase):
    """Garante que a API está efetivamente protegida por JWT."""

    def setUp(self):
        self.user = User.objects.create_user(username='vendedor', password='senha-forte-123')

    def test_acesso_sem_token_bloqueado(self):
        """Sem credenciais, a API nega o acesso."""
        client = APIClient()
        response = client.get('/api/produtos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_e_acesso_com_token(self):
        """O login JWT emite um token que efetivamente autentica na API."""
        client = APIClient()
        login = client.post('/api/auth/login',
                            {'username': 'vendedor', 'password': 'senha-forte-123'}, format='json')
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn('access', login.data)

        token = login.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get('/api/produtos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_credenciais_invalidas(self):
        client = APIClient()
        response = client.post('/api/auth/login',
                              {'username': 'vendedor', 'password': 'errada'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
