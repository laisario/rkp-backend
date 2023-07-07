from rest_framework import permissions, viewsets

from .models import Instrumento
from .serializers import InstrumentoSerializer


class InstrumentoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstrumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Instrumento.objects.filter(cliente__usuario=self.request.user)
