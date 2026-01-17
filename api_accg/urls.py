
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from associados.views import AssociadoViewSet
from financeiro.views import PlanoDeContasViewSet

router = DefaultRouter()
router.register(
    r'associados', AssociadoViewSet, basename='associados',)

router.register(
    r'planos-contas',
    PlanoDeContasViewSet,
    basename='planos-contas'
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

# visualizar os arquivos enviados no navegador durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)