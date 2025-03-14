# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Directions(models.Model):
    nom_direction = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'directions'


class IndicateurPerformance(models.Model):
    id_kpi = models.AutoField(primary_key=True)
    projet = models.ForeignKey('Projets', models.DO_NOTHING, blank=True, null=True)
    nom_indicateurs = models.CharField(max_length=50)
    valeur_cible = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valeur_actuelle = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_maj = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicateur_performance'


class Projets(models.Model):
    id_projets = models.AutoField(primary_key=True)
    nom_projet = models.CharField(max_length=50)
    description_projet = models.TextField(blank=True, null=True)
    directions = models.ForeignKey(Directions, models.DO_NOTHING, blank=True, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    statut_projet = models.CharField(max_length=20, blank=True, null=True)
    chef_projet = models.ForeignKey('Utilisateurs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projets'


class Rapports(models.Model):
    id_rapports = models.AutoField(primary_key=True)
    projet = models.ForeignKey(Projets, models.DO_NOTHING, blank=True, null=True)
    nom_rapport = models.CharField(max_length=50)
    fichier_url = models.TextField()
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rapports'


class Taches(models.Model):
    id_taches = models.AutoField(primary_key=True)
    projet = models.ForeignKey(Projets, models.DO_NOTHING, blank=True, null=True)
    nom_taches = models.CharField(max_length=100)
    description_taches = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey('Utilisateurs', models.DO_NOTHING, blank=True, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    status_taches = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taches'


class Utilisateurs(models.Model):
    nom = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mot_de_passe = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    date_creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'utilisateurs'


class UtilisateursDirections(models.Model):
    utilisateur = models.OneToOneField(Utilisateurs, models.DO_NOTHING, primary_key=True)  # The composite primary key (utilisateur_id, direction_id) found, that is not supported. The first column is selected.
    direction = models.ForeignKey(Directions, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'utilisateurs_directions'
        unique_together = (('utilisateur', 'direction'),)
