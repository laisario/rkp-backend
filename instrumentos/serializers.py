from rest_framework import serializers

from .models import Calibracao, Instrumento, Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class CalibracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calibracao
        fields = "__all__"


class InstrumentoSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    calibracoes = CalibracaoSerializer(many=True)

    class Meta:
        model = Instrumento
        exclude = ["cliente"]
