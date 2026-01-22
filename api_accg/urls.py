from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/associados/', include('associados.urls')),
    path('api/financeiro/', include('financeiro.urls')),
    path('api/cobranca/', include('cobranca.urls')),
]