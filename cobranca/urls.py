from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cobranca.views import CobrancaViewSet
from .webhooks import WebhookPagamentoView


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('webhook/', WebhookPagamentoView.as_view(), name='webhook-pagamento'),
]

router.register(
    r'cobrancas',
    CobrancaViewSet,
    basename='cobrancas'
)
