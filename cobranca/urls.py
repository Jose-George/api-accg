from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CobrancaViewSet
from .webhooks import webhook_pagamento

router = DefaultRouter()
router.register(r'faturas', CobrancaViewSet, basename='cobranca')

urlpatterns = [
    path('', include(router.urls)),
    # Rota manual para o webhook
    path('webhook/pagamento/', webhook_pagamento, name='webhook_pagamento'),
]