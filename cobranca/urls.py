from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CobrancaViewSet
from .webhooks import WebhookPagamentoView


router = DefaultRouter()
router.register(
    r"cobrancas",
    CobrancaViewSet,
    basename="cobrancas",
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "webhook/",
        WebhookPagamentoView.as_view(),
        name="webhook-pagamento",
    ),
]