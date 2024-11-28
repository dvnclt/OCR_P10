from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='authored_projects')

    def __str__(self):
        return self.name


class Contributor(models.Model):
    ROLE_CHOICES = [
        ('AUTHOR', 'Author'),
        ('CONTRIBUTOR', 'Contributor'),
    ]
    # Utilisateur qui contribue
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='contributions')
    # Projet auquel il contribue
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='contributors')
    # Rôle dans le projet
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,
                            default='CONTRIBUTOR')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Empêche les doublons, garanti unicité des relations 'user-project'
        unique_together = ('user', 'project')
        verbose_name = "Contributor"

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
