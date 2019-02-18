import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locadora.settings.development')

django.setup()

from core.models import User, Perfil, Cliente, Midia, Distribuidora, Estado, Cidade, \
Endereco, Genero, Filme, Artista, Item

# genero

genero, created_gen = Genero.objects.get_or_create(nome='Genero 1', slug='gen1')
# Criando usuário
try:
    u = User.objects.get(email='teste@bdd.com')
except User.DoesNotExist:
    u = User.objects.create_superuser(
        email='teste@bdd.com', password='123456', first_name='teste', last_name="bdd"
    )
    u.save()
    u.perfil.cpf = "32808972032"
    u.perfil.data_nascimento="2019-02-01"
    u.perfil.sexo="F"
    u.save()


# Criando cliente padrão
u_cliente, created = User.objects.get_or_create(
    first_name='cliente', last_name='padrão', email='emaildocliente@bdd.com'
)
cliente, created_cli = Cliente.objects.get_or_create(user=u_cliente)

# Criando tipo de midia
midia, created_mid = Midia.objects.get_or_create(nome='DVD', valor=7.5)

# Estado cidade
estado, created_est = Estado.objects.get_or_create(nome='Pernambuco', sigla='PE')
cidade, created_cid = Cidade.objects.get_or_create(nome='Recife', capital=True, estado=estado)

#  Distribuidora
endereco, created_end = Endereco.objects.get_or_create(
    logradouro='Endereço dist',
    numero=10,
    bairro='Bairro dist',
    cep='66600111',
    estado=estado,
    cidade=cidade
)
distribuidora, created_dist = Distribuidora.objects.get_or_create(razao_social='Distribuidora 1', endereco=endereco)

# Filme
diretor, created_dir = Artista.objects.get_or_create(nome='Diretor 1')
ator, created_ator = Artista.objects.get_or_create(nome='Ator 1')

filme, created_fil = Filme.objects.get_or_create(
    titulo='Filme 1', titulo_original='one movie', sinopse='Resumo',
    classificacao='L',duracao='02:00', ano=2018,
    distribuidora=distribuidora, is_lancamento=True
)

filme.genero.add(genero)
filme.diretor.add(diretor)
filme.save()

# Item

item, created = Item.objects.get_or_create(
    numero_serie='1111111', data_aquisicao='2019-02-01', tipo_midia=midia, filme=filme
)