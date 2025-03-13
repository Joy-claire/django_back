from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # L'interface d'administration Django
    path('api/', include('appProjet2.urls')),  # Routes de l'application sous /api/
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Récupération du token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rafraîchissement du token


]
