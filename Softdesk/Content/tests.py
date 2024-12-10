from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project, Contributor

User = get_user_model()


# Test le modèle 'Projet'
class ProjectModelTestCase(TestCase):
    # Configure l'environnement
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='1234',
                                             date_of_birth='2002-11-22')

    # Vérifie le bon fonctionnement de la création d'un objet 'Projet'
    def test_project_creation(self):
        project = Project.objects.create(name='Test Project',
                                         description='A test project',
                                         author=self.user,
                                         type='Back-end')
        # Vérifie que le nom du projet est bien celui renseigné
        self.assertEqual(project.name, 'Test Project')
        # Vérifie que l'auteur du projet est bien l'user instancié
        self.assertEqual(project.author, self.user)


# Test le modèle 'Contributor'
class ContributorModelTestCase(TestCase):
    # Configure l'environnement
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='1234',
                                             date_of_birth='2002-11-22')
        self.project = Project.objects.create(name='Test Project',
                                              description='A test project',
                                              author=self.user,
                                              type='Back-end')

    # Vérifie le bon fonctionnement de la création d'un objet 'Contributor'
    def test_contributor_creation(self):
        contributor = Contributor.objects.create(
            user=self.user,
            project=self.project,
            role='AUTHOR'
        )
        self.assertEqual(contributor.role, 'AUTHOR')
