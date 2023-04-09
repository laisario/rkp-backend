from rest_framework import viewsets
from rest_framework import permissions
from .models import Instrumento
from clientes.models import Cliente
from .serializers import InstrumentoSerializer


class InstrumentoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstrumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cliente = Cliente.objects.filter(usuario=self.request.user).first()
        if cliente:
            return cliente.instrumentos
        return Instrumento.objects.none()
