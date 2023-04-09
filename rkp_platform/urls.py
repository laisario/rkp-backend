"""rkp_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
 
from instrumentos.views import InstrumentoViewSet
from clientes.views import LoginView, RegisterView


router = DefaultRouter()
router.register(r'instrumentos', InstrumentoViewSet, basename='instrumento')

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
    path('register/', RegisterView.as_view(), name='register'),
    path("", include(router.urls)),
    prefix_default_language=False
)
