from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanoDeContasViewSet

router = DefaultRouter()
router.register(r'plano-de-contas', PlanoDeContasViewSet, basename='planodecontas')

urlpatterns = [
    path('', include(router.urls)),
]