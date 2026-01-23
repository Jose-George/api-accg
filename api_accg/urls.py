from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Imports das suas Views
from associados.views import AssociadoViewSet
from financeiro.views import PlanoDeContasViewSet
from users.views import UserViewSet

# Configuração do Router
router = DefaultRouter()
router.register(r'associados', AssociadoViewSet, basename='associados')
router.register(r'users', UserViewSet, basename='users')
router.register(r'planos-contas', PlanoDeContasViewSet, basename='planos-contas')

urlpatterns = [
    # Admin (Apenas uma vez)
    path('admin/', admin.site.urls),
    
    # Autenticação do DRF
    path('api-auth/', include('rest_framework.urls')),
    
    # Rotas da API (O router centraliza as views registradas acima)
    path('api/', include(router.urls)),
    
    # Rotas específicas de apps que não usam o router central
    path('api/', include('cobranca.urls')),
    
    # Documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)