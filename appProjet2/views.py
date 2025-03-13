from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Projets, Taches, Rapports, Directions, Utilisateurs
from .serializers import ProjetSerializer, TacheSerializer, RapportSerializer, DirectionSerializer, UtilisateurSerializer, TokenObtainPairSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UtilisateurSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response



class RegisterView(APIView):
    """
    Vue pour l'inscription des utilisateurs.
    """
    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print("\n🔍 [View] Requête reçue pour /api/token/")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_response = serializer.validated_data  # Ce que retourne le serializer
        user = serializer.user  

        print(f"🔍 [View] Utilisateur: {user.email} (ID: {user.id})")
        print(f"🔍 [View] Rôle: {getattr(user, 'role', '❌ Aucun rôle')}")

        return Response({
            "access": token_response["access"],
            "refresh": token_response["refresh"],
            "role": getattr(user, 'role', '❌ Aucun rôle')  # On force l'affichage du rôle ici
        })


@api_view(['GET'])
def project_detail(request, id_projets):
    try:
        projet = Projets.objects.get(id=id_projets)
        serializer = ProjetSerializer(projet)

        # Compter toutes les tâches principales (celles qui n'ont pas de parent)
        nombre_taches_principales = Taches.objects.filter(projet=projet, parent_tache__isnull=True).count()

        # Compter toutes les sous-tâches (celles qui ont un parent)
        nombre_sous_taches = Taches.objects.filter(projet=projet, parent_tache__isnull=False).count()

        data = serializer.data
        data['nombre_taches'] = nombre_taches_principales  # Nombre total de tâches principales
        data['nombre_sous_taches'] = nombre_sous_taches  # Nombre total de sous-tâches

        return Response(data)

    except Projets.DoesNotExist:
        return Response({"error": "Projet introuvable"}, status=404)

# ✅ API pour les Directions (accessible uniquement aux utilisateurs authentifiés)
class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Directions.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [AllowAny]


# ✅ API pour les Utilisateurs (uniquement admin)
class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateurs.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [AllowAny]  # Seul un admin peut accéder


# ✅ API pour les Projets (seulement pour utilisateurs authentifiés)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projets.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Appel de la méthode de création par défaut de Django REST Framework
        response = super().create(request, *args, **kwargs)
        
        # Construire une réponse personnalisée avec les champs ajustés
        response_data = {
            "code": 0,  # `code` doit être inférieur ou égal à 0
            "data": {
                "category": {  # `category` doit être un objet
                    "id": 1, 
                    "name": "Category Example"
                },
                "name": response.data.get('nom_projet', ''),  # Utiliser le nom du projet
                "photoUrls": [],  # Liste vide ou données réelles pour "photoUrls"
                "tags": [],  # Liste vide ou données réelles pour "tags"
                "status": "available",  # Assigner un statut valide : "available", "pending", "sold"
                **response.data  # Ajouter toutes les données de l'objet projet
            }
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)

# ✅ API pour les Tâches (seulement pour utilisateurs authentifiés)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Taches.objects.all()
    serializer_class = TacheSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        parent_tache_id = request.data.get("parent_tache")

        if parent_tache_id:  # On vérifie seulement si un parent est fourni
            if not isinstance(parent_tache_id, int):
                return Response({"error": "ID invalide"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                parent_tache = Taches.objects.get(id=parent_tache_id)
            except Taches.DoesNotExist:
                return Response({"error": "La tâche parente n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


# ✅ API pour les Rapports (seulement admin)
class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = Rapports.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [AllowAny]  # Restreint aux administrateurs


# ✅ Test API (accessible à tous)
def test_api(request):
    return JsonResponse({"message": "API en ligne et fonctionnelle"})
