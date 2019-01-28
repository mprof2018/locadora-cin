from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from core.views.cruds_views import *
from mixer.backend.django import mixer
import pytest
from django.test import TestCase

@pytest.mark.django_db
class TestGeneroViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestGeneroViews, cls).setUpClass()
        cls.genero = mixer.blend('core.Genero')
        cls.factory = RequestFactory()
    
    def test_genero_lista(self):
        path = reverse('core:genero-listar')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = GeneroListar.as_view()(request)
        assert response.status_code == 200
        print(response)
        # assert 'core/genero/lista.html' in response.url
        # self.assertEqual(response.url, 'core/genero/lista.html')
        
    
    def test_genero_novo(self):
        path = reverse('core:genero-novo')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = GeneroCriar.as_view()(request)
        assert response.status_code == 200
    
    def test_genero_detalhe(self):
        path = reverse('core:genero-detalhe', kwargs={'pk': self.genero.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = GeneroDetalhe.as_view()(request, pk=self.genero.pk)
        assert response.status_code == 200
    
    def test_genero_editar(self):
        path = reverse('core:genero-editar', kwargs={'pk': self.genero.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = GeneroEditar.as_view()(request, pk=self.genero.pk)
        assert response.status_code == 200
    
    def test_genero_deletar(self):
        path = reverse('core:genero-deletar', kwargs={'pk': self.genero.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = GeneroDeletar.as_view()(request, pk=self.genero.pk)
        assert response.status_code == 200


@pytest.mark.django_db
class TestFilmeViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestFilmeViews, cls).setUpClass()
        cls.filme = mixer.blend('core.Filme')
        cls.factory = RequestFactory()
    
    def test_filme_lista(self):
        path = reverse('core:filme-listar')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = FilmeListar.as_view()(request)
        assert response.status_code == 200
        
    
    def test_filme_novo(self):
        path = reverse('core:filme-novo')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = criar_filme(request)
        assert response.status_code == 200
    
    def test_filme_detalhe(self):
        path = reverse('core:filme-detalhe', kwargs={'pk': self.filme.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = FilmeDetalhe.as_view()(request, pk=self.filme.pk)
        assert response.status_code == 200
    
    def test_filme_editar(self):
        path = reverse('core:filme-editar', kwargs={'pk': self.filme.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = editar_filme(request, pk=self.filme.pk)
        assert response.status_code == 200
    
    def test_filme_deletar(self):
        path = reverse('core:filme-deletar', kwargs={'pk': self.filme.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = FilmeDeletar.as_view()(request, pk=self.filme.pk)
        assert response.status_code == 200

@pytest.mark.django_db
class TestMidiaViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestMidiaViews, cls).setUpClass()
        cls.midia = mixer.blend('core.Midia')
        cls.factory = RequestFactory()
    
    def test_midia_lista(self):
        path = reverse('core:midia-listar')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = MidiaListar.as_view()(request)
        assert response.status_code == 200
        
    
    def test_midia_novo(self):
        path = reverse('core:midia-novo')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = MidiaCriar.as_view()(request)
        assert response.status_code == 200
    
    def test_midia_detalhe(self):
        path = reverse('core:midia-detalhe', kwargs={'pk': self.midia.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = MidiaDetalhe.as_view()(request, pk=self.midia.pk)
        assert response.status_code == 200
    
    def test_midia_editar(self):
        path = reverse('core:midia-editar', kwargs={'pk': self.midia.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = MidiaEditar.as_view()(request, pk=self.midia.pk)
        assert response.status_code == 200
    
    def test_midia_deletar(self):
        path = reverse('core:midia-deletar', kwargs={'pk': self.midia.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = MidiaDeletar.as_view()(request, pk=self.midia.pk)
        assert response.status_code == 200


@pytest.mark.django_db
class TestArtistaViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestArtistaViews, cls).setUpClass()
        cls.artista = mixer.blend('core.Artista')
        cls.factory = RequestFactory()
    
    def test_artista_lista(self):
        path = reverse('admin:artista-listar')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = ArtistaListar.as_view()(request)
        assert response.status_code == 200
        
    
    def test_artista_novo(self):
        path = reverse('admin:artista-novo')
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = ArtistaCriar.as_view()(request)
        assert response.status_code == 200
    
    def test_artista_detalhe(self):
        path = reverse('admin:artista-detalhe', kwargs={'pk': self.artista.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = ArtistaDetalhe.as_view()(request, pk=self.artista.pk)
        assert response.status_code == 200
    
    def test_artista_editar(self):
        path = reverse('admin:artista-editar', kwargs={'pk': self.artista.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = ArtistaEditar.as_view()(request, pk=self.artista.pk)
        assert response.status_code == 200
    
    def test_artista_deletar(self):
        path = reverse('admin:artista-deletar', kwargs={'pk': self.artista.pk})
        request = self.factory.get(path)
        # request.user = mixer.blend(User)

        response = ArtistaDeletar.as_view()(request, pk=self.artista.pk)
        assert response.status_code == 200