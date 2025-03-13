from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateurs, Directions, Projets, Taches, Rapports

class CustomUserAdmin(UserAdmin):
    # Champs affichés dans l'admin
    list_display = ('email', 'nom', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'nom')
    ordering = ['email']  # Correction : on trie par email au lieu de username
    
    # Définition des champs affichés dans le formulaire d'édition d'un utilisateur
    fieldsets = UserAdmin.fieldsets + (
        ("Rôles et permissions", {'fields': ('role',)}),  # Correction : virgule ajoutée
    )

    # Permissions d'accès au module Utilisateurs
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.role == 'Admin'

    # Permissions sur les actions (ajouter, modifier, supprimer)
    def has_add_permission(self, request):
        return request.user.has_perm('appProjet2.add_projet')  # Correction : utilisation de `has_perm`

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('appProjet2.change_projet')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('appProjet2.delete_projet')

# Enregistrement des modèles dans l'admin
admin.site.register(Utilisateurs, CustomUserAdmin)
admin.site.register(Directions)
admin.site.register(Projets)
admin.site.register(Taches)
admin.site.register(Rapports)
