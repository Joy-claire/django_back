from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, AuditLogViewSet, DirectionViewSet, UtilisateurViewSet,  RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView , project_detail # Import de la vue personnalisée

# Création du routeur DRF pour générer automatiquement les routes
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)  # API pour les Projets
router.register(r'tasks', TaskViewSet)  # API pour les Tâches
router.register(r'rapports', AuditLogViewSet)  # API pour les Rapports
router.register(r'directions', DirectionViewSet)  # API pour les Directions
router.register(r'utilisateurs', UtilisateurViewSet)  # API pour les Utilisateurs

# Définition des URL de l'application
urlpatterns = [
    path('', include(router.urls)),  # Inclure toutes les routes du routeur automatiquement
    path('register/', RegisterView.as_view(), name='api-register'),  # Ajout de l'endpoint register
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/projects/<int:id_projets>/', project_detail, name='project-detail'),

]