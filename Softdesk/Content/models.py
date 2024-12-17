import uuid

from django.db import models
from User.models import User


class Project(models.Model):
    TYPE_CHOICES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='authored_projects')
    type = models.CharField(max_length=20,
                            choices=TYPE_CHOICES,
                            null=False,
                            blank=False)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    ROLE_CHOICES = [
        ('AUTHOR', 'Author'),
        ('CONTRIBUTOR', 'Contributor'),
    ]
    # Utilisateur qui contribue
    user = models.ForeignKey(User,
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

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                                related_name='issues')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='authored_issues')
    assigned_to = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='assigned_issues')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES,
                                null=True, default='MEDIUM')
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, null=True,
                           default='TASK')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=True,
                              default='TODO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    issue = models.ForeignKey(Issue, related_name='comments',
                              on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commentaire de {self.author} pour {self.issue.title}"
