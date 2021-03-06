from django.urls import reverse, resolve

class TestUrls:
    
    # Início CRUD Gênero
    def test_genero_listar(self):
        path = reverse('core:genero-listar')
        assert resolve(path).view_name == 'core:genero-listar'

    def test_genero_novo(self):
        path = reverse('core:genero-novo')
        assert resolve(path).view_name == 'core:genero-novo'

    def test_genero_editar(self):
        path = reverse('core:genero-editar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:genero-editar'

    def test_genero_detalhe(self):
        path = reverse('core:genero-detalhe', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:genero-detalhe'

    def test_genero_deletar(self):
        path = reverse('core:genero-deletar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:genero-deletar'
    # Termino CRUD Gênero

    # Início CRUD Filme
    def test_filme_listar(self):
        path = reverse('core:filme-listar')
        assert resolve(path).view_name == 'core:filme-listar'

    def test_filme_novo(self):
        path = reverse('core:filme-novo')
        assert resolve(path).view_name == 'core:filme-novo'

    def test_filme_editar(self):
        path = reverse('core:filme-editar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:filme-editar'

    def test_filme_detalhe(self):
        path = reverse('core:filme-detalhe', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:filme-detalhe'

    def test_filme_deletar(self):
        path = reverse('core:filme-deletar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:filme-deletar'
    
    # Termino CRUD Filme
    
    # Início CRUD Midia
    def test_midia_listar(self):
        path = reverse('core:midia-listar')
        assert resolve(path).view_name == 'core:midia-listar'

    def test_midia_novo(self):
        path = reverse('core:midia-novo')
        assert resolve(path).view_name == 'core:midia-novo'

    def test_midia_editar(self):
        path = reverse('core:midia-editar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:midia-editar'

    def test_midia_detalhe(self):
        path = reverse('core:midia-detalhe', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:midia-detalhe'

    def test_midia_deletar(self):
        path = reverse('core:midia-deletar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:midia-deletar'
    
    # Início CRUD Artista
    def test_artista_listar(self):
        path = reverse('core:artista-listar')
        assert resolve(path).view_name == 'core:artista-listar'

    def test_artista_novo(self):
        path = reverse('core:artista-novo')
        assert resolve(path).view_name == 'core:artista-novo'

    def test_artista_editar(self):
        path = reverse('core:artista-editar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:artista-editar'

    def test_artista_detalhe(self):
        path = reverse('core:artista-detalhe', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:artista-detalhe'

    def test_artista_deletar(self):
        path = reverse('core:artista-deletar', kwargs={'pk' : 1})
        assert resolve(path).view_name == 'core:artista-deletar'

    #Ajax
    def test_diretor_ajax_novo(self):
        path = reverse('core:ajax-diretor-novo')
        assert resolve(path).view_name == 'core:ajax-diretor-novo'
    
    def test_ator_ajax_novo(self):
        path = reverse('core:ajax-ator-novo')
        assert resolve(path).view_name == 'core:ajax-ator-novo'

    def test_genero_ajax_novo(self):
        path = reverse('core:ajax-genero-novo')
        assert resolve(path).view_name == 'core:ajax-genero-novo'
