from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Cliente, Empresa, Unidade
from enderecos.models import Bairro, Cidade, Endereco, UF


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)
        if hasattr(user, 'cliente'):
            token['nome'] = user.cliente.__str__()
        return token


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    nome = serializers.CharField(required=False, write_only=True)
    telefone = serializers.CharField(required=False, write_only=True)
    cpf = serializers.CharField(required=False, write_only=True)

    empresa = serializers.BooleanField(default=False, write_only=True)
    razao_social = serializers.CharField(required=False, write_only=True)
    cnpj = serializers.CharField(required=False, write_only=True)
    ie = serializers.CharField(required=False, write_only=True)
    isento = serializers.BooleanField(default=False, write_only=True)

    uf = serializers.CharField(write_only=True)
    cidade = serializers.CharField(write_only=True)
    bairro = serializers.CharField(write_only=True)
    logradouro = serializers.CharField(write_only=True)
    numero = serializers.IntegerField(write_only=True)
    complemento = serializers.CharField(required=False, write_only=True)
    cep = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
        )
        empresa = None
        user.set_password(validated_data['password'])
        user.save()
        if validated_data.get('empresa'):
            empresa, created = Empresa.objects.get_or_create(
                razao_social=validated_data.get('razao_social'),
                cnpj=validated_data.get('cnpj'),
                ie=validated_data.get('ie'),
                isento=validated_data.get('isento')
            )
            for unidade in validated_data.get('unidades', []):
                Unidade.objects.create(nome=unidade, empresa=empresa)

        uf, created = UF.objects.get_or_create(sigla=validated_data.get('uf'))
        cidade, created = Cidade.objects.get_or_create(
            uf=uf,
            nome=validated_data.get('cidade')
        )
        bairro, created = Bairro.objects.get_or_create(
            cidade=cidade,
            nome=validated_data.get('bairro')
        )
        endereco, created = Endereco.objects.get_or_create(
            cep=validated_data.get('cep'),
            numero=validated_data.get('numero'),
            bairro=bairro,
            logradouro=validated_data.get('logradouro'),
            complemento=validated_data.get("complemento", '')
        )

        Cliente.objects.create(
            usuario=user,
            nome=validated_data.get('nome'),
            telefone=validated_data.get('telefone'),
            cpf=validated_data.get('cpf'),
            endereco=endereco,
            empresa=empresa,
        )

        return user


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"


class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = "__all__"
