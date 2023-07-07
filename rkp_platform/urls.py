from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from clientes.views import LoginView, RegisterView
from instrumentos.views import InstrumentoViewSet

router = DefaultRouter()
router.register(r"instrumentos", InstrumentoViewSet, basename="instrumento")

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    prefix_default_language=False,
)
