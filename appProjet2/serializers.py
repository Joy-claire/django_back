from rest_framework import serializers
from .models import Projets, Taches, Rapports, Directions, Utilisateurs
from .models import Utilisateurs
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class DirectionSerializer(serializers.ModelSerializer):
    """
    Ce serializer permet de transformer les instances du modèle Directions en données JSON.
    """
    class Meta:
        model = Directions
        fields = '__all__'  # Tous les champs de Directions

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("🔍 [Serializer] Début validation...")
        
        data = super().validate(attrs)  # Génération des tokens
        user = self.user  # Récupération de l'utilisateur
        
        # 🔍 Debugging avancé
        print(f"🔍 [Serializer] Utilisateur trouvé: {user.email} (ID: {user.id})")
        print(f"🔍 [Serializer] Rôle récupéré: {getattr(user, 'role', '❌ Aucun rôle trouvé')}")

        # Forcer le retour du rôle
        data['role'] = getattr(user, 'role', '❌ Aucun rôle trouvé')

        return data



class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Ce serializer permet de transformer les instances du modèle Utilisateurs en données JSON.
    """
    class Meta:
        model = Utilisateurs
        fields = ['id', 'nom', 'email', 'role', 'date_creation', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Masquer le mot de passe en lecture

    def create(self, validated_data):
        # Hasher le mot de passe avant de créer l'utilisateur
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

class ProjetSerializer(serializers.ModelSerializer):
    """
    Ce serializer transforme les instances du modèle Project en données JSON et inversement.
    """
    class Meta:
        model = Projets
        fields = '__all__'

class TacheSerializer(serializers.ModelSerializer):
    """
    Ce serializer s'occupe de la conversion des instances du modèle Task.
    """
    class Meta:
        model = Taches
        fields = '__all__'

class RapportSerializer(serializers.ModelSerializer):
    """
    Ce serializer permet de transformer les logs d'audit (AuditLog) en JSON.
    """
    class Meta:
        model = Rapports
        fields = '__all__'
