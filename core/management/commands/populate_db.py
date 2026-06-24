import random
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import Cliente, Produto, Venda, ItemVenda

User = get_user_model()

CLIENTES = [
    ("Ana Paula Rodrigues",     "123.456.789-01", "ana.rodrigues@gmail.com",   "(11) 98234-5678", "Rua das Flores, 120 - São Paulo/SP"),
    ("Carlos Eduardo Lima",     "234.567.890-12", "carlos.lima@hotmail.com",   "(21) 97123-4567", "Av. Atlântica, 800 - Rio de Janeiro/RJ"),
    ("Fernanda Costa Mendes",   "345.678.901-23", "fernanda.mendes@gmail.com", "(31) 96012-3456", "Rua Sapucaí, 45 - Belo Horizonte/MG"),
    ("Ricardo Alves Souza",     "456.789.012-34", "ricardo.souza@outlook.com", "(41) 95901-2345", "Av. Batel, 1200 - Curitiba/PR"),
    ("Juliana Ferreira Nunes",  "567.890.123-45", "juliana.nunes@gmail.com",   "(51) 94890-1234", "Rua Padre Chagas, 88 - Porto Alegre/RS"),
    ("Marcos Vinícius Pereira", "678.901.234-56", "marcos.pereira@gmail.com",  "(61) 93789-0123", "SQN 215, Bloco C - Brasília/DF"),
    ("Camila Oliveira Dias",    "789.012.345-67", "camila.dias@icloud.com",    "(71) 92678-9012", "Av. Tancredo Neves, 340 - Salvador/BA"),
    ("Thiago Santos Barros",    "890.123.456-78", "thiago.barros@gmail.com",   "(81) 91567-8901", "Av. Boa Viagem, 2500 - Recife/PE"),
    ("Larissa Monteiro Silva",  "901.234.567-89", "larissa.silva@gmail.com",   "(85) 99456-7890", "Av. Beira Mar, 650 - Fortaleza/CE"),
    ("Felipe Gomes Cardoso",    "012.345.678-90", "felipe.cardoso@hotmail.com","(92) 98345-6789", "Rua Recife, 78 - Manaus/AM"),
    ("Beatriz Ramos Teixeira",  "111.222.333-44", "beatriz.teixeira@gmail.com","(11) 97234-5670", "Rua Augusta, 500 - São Paulo/SP"),
    ("Gabriel Henrique Castro", "222.333.444-55", "gabriel.castro@gmail.com",  "(19) 96123-4560", "Av. Brasil, 1100 - Campinas/SP"),
    ("Amanda Lopes Freitas",    "333.444.555-66", "amanda.freitas@outlook.com","(27) 95012-3450", "Av. Vitória, 220 - Vitória/ES"),
    ("Leonardo Nascimento Cruz","444.555.666-77", "leonardo.cruz@gmail.com",   "(62) 94901-2340", "Av. T-63, 1800 - Goiânia/GO"),
    ("Patrícia Moura Ribeiro",  "555.666.777-88", "patricia.ribeiro@gmail.com","(83) 93890-1230", "Rua João Pessoa, 300 - João Pessoa/PB"),
    ("Rodrigo Carvalho Martins","666.777.888-99", "rodrigo.martins@icloud.com","(98) 92789-0120", "Av. dos Holandeses, 900 - São Luís/MA"),
    ("Isabela Pinto Araújo",    "777.888.999-00", "isabela.araujo@gmail.com",  "(86) 91678-9010", "Av. Frei Serafim, 1500 - Teresina/PI"),
    ("Bruno Azevedo Correia",   "888.999.000-11", "bruno.correia@hotmail.com", "(91) 99567-8900", "Travessa Padre Eutíquio, 600 - Belém/PA"),
    ("Natália Cunha Menezes",   "999.000.111-22", "natalia.menezes@gmail.com", "(94) 98456-7890", "Av. Presidente Médici, 400 - Santarém/PA"),
    ("Diego Tavares Braga",     "100.200.300-40", "diego.braga@gmail.com",     "(67) 97345-6780", "Av. Afonso Pena, 650 - Campo Grande/MS"),
    ("Renata Campos Borges",    "200.300.400-50", "renata.borges@outlook.com", "(65) 96234-5670", "Av. do CPA, 300 - Cuiabá/MT"),
    ("André Rocha Figueiredo",  "300.400.500-60", "andre.figueiredo@gmail.com","(68) 95123-4560", "Rua Marechal Deodoro, 180 - Rio Branco/AC"),
    ("Vanessa Leite Andrade",   "400.500.600-70", "vanessa.andrade@gmail.com", "(96) 94012-3450", "Av. Presidente Vargas, 1200 - Macapá/AP"),
    ("Gustavo Brito Machado",   "500.600.700-80", "gustavo.machado@icloud.com","(95) 93901-2340", "Av. das Acácias, 800 - Boa Vista/RR"),
    ("Mônica Duarte Cavalcante","600.700.800-90", "monica.cavalcante@gmail.com","(79) 92890-1230","Av. Delmiro Gouveia, 450 - Aracaju/SE"),
]

PRODUTOS = [
    # (nome, descricao, categoria, preco, estoque, estoque_minimo)
    ("iPhone 15 Pro 256GB",         "Apple iPhone 15 Pro, chip A17 Pro, câmera 48MP, titânio",         "Smartphones",  8_999.00, 18, 3),
    ("Samsung Galaxy S24 Ultra",    "Galaxy S24 Ultra 512GB, câmera 200MP, S Pen incluso",              "Smartphones",  7_499.00, 14, 3),
    ("Xiaomi 14 Pro 256GB",         "Xiaomi 14 Pro, Snapdragon 8 Gen 3, câmera Leica",                 "Smartphones",  4_299.00, 22, 5),
    ("Motorola Edge 50 Pro",        "Motorola Edge 50 Pro, 6.7\" pOLED, carga 125W",                   "Smartphones",  2_799.00, 30, 5),
    ("Google Pixel 9 Pro",          "Google Pixel 9 Pro 128GB, IA generativa integrada",               "Smartphones",  5_999.00, 10, 3),
    ("MacBook Pro 14\" M4",         "MacBook Pro 14\" chip M4 Pro, 18GB RAM, 512GB SSD",               "Notebooks",   16_999.00,  8, 2),
    ("Dell XPS 15 9530",            "Dell XPS 15, Intel Core i9, RTX 4070, 32GB RAM",                  "Notebooks",   12_499.00,  6, 2),
    ("Lenovo ThinkPad X1 Carbon",   "ThinkPad X1 Carbon Gen 12, i7, 16GB, 512GB SSD, leve",           "Notebooks",    9_299.00,  9, 2),
    ("ASUS ROG Zephyrus G16",       "ROG Zephyrus G16, Ryzen 9, RTX 4080, 240Hz",                     "Notebooks",   14_799.00,  5, 2),
    ("Acer Swift Go 14",            "Acer Swift Go 14, Intel Core Ultra 7, OLED, 16GB",                "Notebooks",    5_799.00, 12, 3),
    ("iPad Pro 13\" M4",            "iPad Pro 13\" chip M4, OLED, Wi-Fi + Cellular 256GB",             "Tablets",      9_499.00, 10, 2),
    ("Samsung Galaxy Tab S9 Ultra", "Galaxy Tab S9 Ultra 14.6\", S Pen, 256GB",                       "Tablets",      6_999.00,  8, 2),
    ("iPad Air 11\" M2",            "iPad Air 11\" chip M2, Wi-Fi 128GB, azul",                       "Tablets",      5_299.00, 15, 3),
    ("Lenovo Tab P12 Pro",          "Tab P12 Pro 12.6\" AMOLED, 8GB RAM, 256GB",                      "Tablets",      3_499.00, 11, 3),
    ("Samsung Galaxy Tab A9+",      "Galaxy Tab A9+ 11\", 4GB RAM, 64GB, Wi-Fi",                      "Tablets",      1_799.00, 20, 5),
    ("Sony WH-1000XM5",             "Fone over-ear, cancelamento de ruído líder de mercado",           "Áudio",        1_899.00, 25, 5),
    ("AirPods Pro 2ª Geração",      "AirPods Pro com chip H2, cancelamento ativo, MagSafe",            "Áudio",        2_099.00, 20, 5),
    ("JBL Charge 5",                "Caixa Bluetooth portátil, 20h bateria, resistente à água",        "Áudio",          799.00, 35, 8),
    ("Bose QuietComfort 45",        "Fone over-ear Bose QC45, ANC, 24h bateria",                       "Áudio",        1_699.00, 18, 4),
    ("Sony SRS-XB100",              "Caixinha Bluetooth compacta, IP67, 16h bateria",                  "Áudio",          349.00, 50, 10),
    ("Samsung Neo QLED 55\" 8K",    "Smart TV Neo QLED 8K 55\", Tizen, 120Hz",                        "TVs",          8_999.00,  5, 1),
    ("LG OLED evo 65\" G4",         "TV OLED evo G4 65\", α11 AI, 120Hz, Dolby Vision",               "TVs",         11_499.00,  4, 1),
    ("Sony Bravia 7 55\"",          "Sony Bravia 7 55\" Mini LED QLED, Google TV",                    "TVs",          5_799.00,  7, 2),
    ("Philips Ambilight 50\"",      "TV 4K Ambilight 50\", Android TV, Dolby Atmos",                  "TVs",          2_999.00, 10, 2),
    ("TCL C845 75\"",               "TCL QLED Mini LED 75\", 144Hz, Google TV",                       "TVs",          4_499.00,  6, 1),
    ("PS5 Slim Digital Edition",    "PlayStation 5 Slim, SSD 1TB, sem leitor de disco",               "Games",        3_799.00, 12, 3),
    ("Xbox Series X 2TB",           "Xbox Series X 2TB, Game Pass Ultimate, 4K 120fps",               "Games",        4_299.00,  8, 2),
    ("Nintendo Switch OLED",        "Nintendo Switch OLED 64GB, tela 7\", dock incluída",             "Games",        2_499.00, 15, 4),
    ("DualSense Edge",              "Controle PS5 DualSense Edge, personalizável, pro",                "Games",          999.00, 20, 5),
    ("Xbox Wireless Controller",    "Controle Xbox sem fio, Robot White, USB-C",                      "Games",          399.00, 30, 8),
    ("Logitech MX Master 3S",       "Mouse sem fio MX Master 3S, 8000 DPI, scroll silencioso",        "Periféricos",    799.00, 28, 6),
    ("Keychron Q3 Pro",             "Teclado mecânico TKL, switch Gateron, RGB, wireless",            "Periféricos",    999.00, 15, 4),
    ("Dell UltraSharp U2723D",      "Monitor 27\" 4K IPS, USB-C 90W, DisplayHDR 400",                "Periféricos",  3_299.00,  9, 2),
    ("Webcam Logitech Brio 4K",     "Webcam 4K Ultra HD, HDR, microfone com ANC",                     "Periféricos",    999.00, 20, 5),
    ("SSD Samsung 990 Pro 2TB",     "SSD NVMe M.2 PCIe 4.0 2TB, 7.450 MB/s leitura",                "Periféricos",    699.00, 22, 6),
    ("Apple Watch Series 9 45mm",   "Apple Watch S9 45mm, chip S9, Always-On, GPS",                  "Wearables",     3_299.00, 14, 3),
    ("Samsung Galaxy Watch 6 Pro",  "Galaxy Watch 6 Classic 47mm, bisel rotativo, GPS",              "Wearables",     2_199.00, 12, 3),
    ("Garmin Forerunner 965",       "Smartwatch running premium, AMOLED, mapas offline",              "Wearables",     4_799.00,  7, 2),
    ("Fitbit Charge 6",             "Fitbit Charge 6, ECG, SpO2, integração Google",                  "Wearables",      999.00, 25, 5),
    ("Xiaomi Smart Band 8 Pro",     "Mi Band 8 Pro, AMOLED 1.74\", GPS nativo, 14 dias bateria",     "Wearables",      499.00, 40, 8),
]

OBSERVACOES = [
    "Cliente preferencial.",
    "Entrega expressa solicitada.",
    "Presente para aniversário.",
    "Compra corporativa.",
    "Cliente indicou programa de fidelidade.",
    "Primeiro pedido do cliente.",
    "Troca de modelo anterior.",
    "Compra para home office.",
    None, None, None, None,  # maioria sem observação
]


class Command(BaseCommand):
    help = "Popula o banco com dados de demonstração para apresentação"

    def handle(self, *args, **kwargs):
        self.stdout.write("Limpando dados anteriores...")
        ItemVenda.objects.all().delete()
        Venda.objects.all().delete()
        Produto.objects.all().delete()
        Cliente.objects.all().delete()

        # --- Clientes ---
        self.stdout.write("Criando clientes...")
        clientes = []
        for nome, cpf, email, tel, end in CLIENTES:
            c = Cliente.objects.create(nome=nome, cpf=cpf, email=email, telefone=tel, endereco=end)
            clientes.append(c)
        self.stdout.write(self.style.SUCCESS(f"  {len(clientes)} clientes criados"))

        # --- Produtos ---
        self.stdout.write("Criando produtos...")
        produtos = []
        for nome, desc, cat, preco, estoque, est_min in PRODUTOS:
            p = Produto.objects.create(
                nome=nome,
                descricao=desc,
                categoria=cat,
                preco=Decimal(str(preco)),
                quantidade_estoque=estoque,
                estoque_minimo=est_min,
                ativo=True,
            )
            produtos.append(p)
        self.stdout.write(self.style.SUCCESS(f"  {len(produtos)} produtos criados"))

        # --- Superusuário para vincular vendas ---
        usuario = User.objects.filter(is_superuser=True).first()
        if not usuario:
            self.stdout.write(self.style.ERROR("Nenhum superusuário encontrado. Rode createsuperuser antes."))
            return

        # --- Vendas distribuídas nos últimos 6 meses ---
        self.stdout.write("Criando vendas...")
        agora = timezone.now()
        total_vendas = 0

        # Distribuição por mês: mais recente tem mais vendas (crescimento)
        meses_config = [
            (180, 150, 8),   # 6 meses atrás — 8 vendas
            (150, 121, 12),  # 5 meses atrás — 12 vendas
            (120, 91,  15),  # 4 meses atrás — 15 vendas
            (90,  61,  18),  # 3 meses atrás — 18 vendas
            (60,  31,  22),  # 2 meses atrás — 22 vendas
            (30,  1,   25),  # último mês    — 25 vendas
        ]

        for dias_max, dias_min, qtd_vendas in meses_config:
            for _ in range(qtd_vendas):
                cliente = random.choice(clientes)
                obs = random.choice(OBSERVACOES)

                venda = Venda.objects.create(
                    cliente=cliente,
                    usuario=usuario,
                    valor_total=Decimal("0"),
                    observacoes=obs,
                )

                # Retrodata a venda
                dias_atras = random.randint(dias_min, dias_max)
                data = agora - timedelta(days=dias_atras, hours=random.randint(0, 23), minutes=random.randint(0, 59))
                Venda.objects.filter(pk=venda.pk).update(data_venda=data)

                # Itens (1 a 4 produtos por venda)
                num_itens = random.randint(1, 4)
                produtos_venda = random.sample(produtos, min(num_itens, len(produtos)))
                valor_total = Decimal("0")

                for produto in produtos_venda:
                    qtd = random.randint(1, 3)
                    # Garante que tem estoque suficiente para o item
                    if produto.quantidade_estoque < qtd:
                        qtd = max(1, produto.quantidade_estoque)
                    subtotal = produto.preco * qtd
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=qtd,
                        preco_unitario=produto.preco,
                        subtotal=subtotal,
                    )
                    valor_total += subtotal
                    produto.quantidade_estoque -= qtd
                    produto.save(update_fields=["quantidade_estoque"])

                Venda.objects.filter(pk=venda.pk).update(valor_total=valor_total)
                total_vendas += 1

        self.stdout.write(self.style.SUCCESS(f"  {total_vendas} vendas criadas"))
        self.stdout.write(self.style.SUCCESS("\nBanco populado com sucesso!"))
        self.stdout.write(f"  Clientes : {Cliente.objects.count()}")
        self.stdout.write(f"  Produtos : {Produto.objects.count()}")
        self.stdout.write(f"  Vendas   : {Venda.objects.count()}")
        self.stdout.write(f"  Itens    : {ItemVenda.objects.count()}")
