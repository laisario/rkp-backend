from rest_framework import serializers


from .models import Bairro, Cidade, Endereco, UF


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = "__all__"


class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = "__all__"


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = "__all__"


class UFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UF
        fields = "__all__"
