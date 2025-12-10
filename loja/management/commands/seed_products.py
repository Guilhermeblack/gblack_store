from django.core.management.base import BaseCommand
from loja.models import Produto


class Command(BaseCommand):
    help = 'Popula a base com 10 produtos de exemplo'

    def handle(self, *args, **options):
        products = [
            # Relógios (R)
            {
                'nome': 'Relógio Masculino Sport Militar Preto Dourado',
                'descricao': 'Relógio masculino esportivo com acabamento preto e detalhes dourados. Resistente à água, ideal para o dia a dia e práticas esportivas.',
                'preco': 189.90,
                'tipo': 'R',
                'estoque': 25,
                'is_available': True,
            },
            {
                'nome': 'Relógio Skmei AnaDigi Premium',
                'descricao': 'Relógio analógico e digital com design moderno. Pulseira de aço inoxidável preta com mostrador dourado.',
                'preco': 249.90,
                'tipo': 'R',
                'estoque': 15,
                'is_available': True,
            },
            {
                'nome': 'Relógio Clássico Executivo Preto',
                'descricao': 'Relógio elegante para ocasiões formais. Pulseira de couro genuíno preto com mostrador minimalista.',
                'preco': 329.90,
                'tipo': 'R',
                'estoque': 10,
                'is_available': True,
            },
            # Acessórios (A)
            {
                'nome': 'Corrente Grossa Aço Inoxidável Preto',
                'descricao': 'Corrente masculina de aço inoxidável com banho preto. 60cm de comprimento, estilo streetwear.',
                'preco': 89.90,
                'tipo': 'A',
                'estoque': 50,
                'is_available': True,
            },
            {
                'nome': 'Kit Pulseiras Couro e Metal',
                'descricao': 'Kit com 3 pulseiras masculinas: 2 de couro trançado e 1 de metal preto. Ajustáveis.',
                'preco': 59.90,
                'tipo': 'A',
                'estoque': 40,
                'is_available': True,
            },
            {
                'nome': 'Anel Signet Preto Fosco',
                'descricao': 'Anel masculino estilo signet em aço inoxidável com acabamento preto fosco. Design minimalista e elegante.',
                'preco': 69.90,
                'tipo': 'A',
                'estoque': 30,
                'is_available': True,
            },
            {
                'nome': 'Conjunto Corrente + Pulseira Black Edition',
                'descricao': 'Conjunto premium com corrente e pulseira combinando. Aço inoxidável preto, perfeito para presente.',
                'preco': 149.90,
                'tipo': 'A',
                'estoque': 20,
                'is_available': True,
            },
            # Vestuário (V)
            {
                'nome': 'Camiseta Oversized Streetwear Preta',
                'descricao': 'Camiseta oversized 100% algodão premium. Modelagem ampla e confortável, perfeita para looks despojados.',
                'preco': 79.90,
                'tipo': 'V',
                'estoque': 60,
                'is_available': True,
            },
            {
                'nome': 'Moletom Hoodie Black Essential',
                'descricao': 'Moletom com capuz em algodão felpado. Modelagem regular, bolso canguru, ideal para dias frios.',
                'preco': 159.90,
                'tipo': 'V',
                'estoque': 35,
                'is_available': True,
            },
            {
                'nome': 'Calça Jogger Streetwear Preta',
                'descricao': 'Calça jogger masculina com elástico no tornozelo. Tecido leve e confortável, bolsos laterais.',
                'preco': 129.90,
                'tipo': 'V',
                'estoque': 45,
                'is_available': True,
            },
        ]

        created_count = 0
        for product_data in products:
            produto, created = Produto.objects.get_or_create(
                nome=product_data['nome'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Produto criado: {produto.nome}'))
            else:
                self.stdout.write(self.style.WARNING(f'Produto já existe: {produto.nome}'))

        self.stdout.write(self.style.SUCCESS(f'\n{created_count} produtos criados com sucesso!'))
