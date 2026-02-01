from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from associados.views import AssociadoViewSet
from financeiro.views import PlanoDeContasViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register(r'associados', AssociadoViewSet, basename='associados')
router.register(r'users', UserViewSet, basename='users')
router.register(r'planos-contas', PlanoDeContasViewSet, basename='planos-contas')

urlpatterns = [
    # Painel Administrativo
    path('admin/', admin.site.urls),
    
    # Autenticação do DRF (Login para browsable API)
    path('api-auth/', include('rest_framework.urls')),
    
    # Rotas Automáticas do Router (Associados, Users, Financeiro)
    path('api/', include(router.urls)),
    
    # Rotas Manuais do App de Cobrança
    path('api/', include('cobranca.urls')),
    
    # Documentação Automática (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Configuração de Mídia (Apenas para ambiente de Desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)