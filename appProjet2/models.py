from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class Directions(models.Model):
    nom_direction = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "directions"
        verbose_name = "Direction"
        verbose_name_plural = "Directions"

    def __str__(self):
        return self.nom_direction


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        
        extra_fields.setdefault('role', 'Employe') 
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Utilisateurs(AbstractUser, PermissionsMixin):
    ROLES = [
        ('Admin', 'Administrateur'),
        ('ChefProjet', 'Chef de Projet'),
        ('Employe', 'Employé'),
        ('UserStandard', 'UserStandard'),

    ]

    username = None  # Supprimer le champ username
    nom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='Employe')
    date_creation = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Utiliser l'email comme identifiant
    REQUIRED_FIELDS = ['nom']  # Champs requis en plus du mot de passe

    objects = CustomUserManager()  # Utilisation du gestionnaire personnalisé

    class Meta:
        db_table = "utilisateurs"
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.nom} ({self.email})"


class UtilisateursDirections(models.Model):
    utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, related_name="directions_affectees")
    direction = models.ForeignKey(Directions, on_delete=models.CASCADE, related_name="membres")

    class Meta:
        unique_together = ('utilisateur', 'direction')
        db_table = "utilisateurs_directions"
        verbose_name = "Affectation Direction"
        verbose_name_plural = "Affectations Directions"

    def __str__(self):
        return f"{self.utilisateur.nom} -> {self.direction.nom_direction}"


class Projets(models.Model):
    STATUTS_PROJET = [
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
        ('Annulé', 'Annulé'),
        ('En attente', 'En attente'),

    ]

    nom_projet = models.CharField(max_length=50)
    description_projet = models.TextField(blank=True, null=True)
    direction = models.ForeignKey(Directions, on_delete=models.SET_NULL, null=True, related_name="projets")
    date_debut = models.DateField()
    date_fin = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    statut_projet = models.CharField(max_length=20, choices=STATUTS_PROJET, blank=True, null=True)
    chef_projet = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, null=True, related_name="projets_geres")

    class Meta:
        permissions = [
            ("add_projet", "Peut ajouter un projet"),
            ("change_projet", "Peut modifier un projet"),
            ("delete_projet", "Peut supprimer un projet"),
            ("view_projet", "Peut voir les projets"),
        ]
        db_table = "projets"
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.nom_projet


class IndicateurPerformance(models.Model):
    projet = models.ForeignKey(Projets, on_delete=models.CASCADE, related_name="indicateurs")
    nom_indicateur = models.CharField(max_length=50)
    valeur_cible = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valeur_actuelle = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_maj = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "indicateur_performance"
        verbose_name = "Indicateur de Performance"
        verbose_name_plural = "Indicateurs de Performance"

    def __str__(self):
        return f"{self.nom_indicateur} ({self.projet.nom_projet})"


class Rapports(models.Model):
    projet = models.ForeignKey(Projets, on_delete=models.CASCADE, related_name="rapports")
    nom_rapport = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='rapports/')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rapports"
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"

    def __str__(self):
        return self.nom_rapport


class Taches(models.Model):
    STATUTS_TACHE = [
        ('À faire', 'À faire'),
        ('En cours', 'En cours'),
        ('En attente', 'En attente'),
        ('Terminée', 'Terminée'),
    ]

    projet = models.ForeignKey(Projets, on_delete=models.CASCADE, related_name="taches")
    nom_tache = models.CharField(max_length=100)
    description_tache = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, null=True, related_name="taches_assignees")
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut_tache = models.CharField(max_length=20, choices=STATUTS_TACHE, blank=True, null=True)
    parent_tache = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sous_taches')

    class Meta:
        db_table = "taches"
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    def __str__(self):
        return self.nom_tache
