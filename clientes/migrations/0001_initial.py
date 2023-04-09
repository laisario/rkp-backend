# Generated by Django 4.2 on 2023-04-04 02:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("enderecos", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Empresa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "razao_social",
                    models.CharField(max_length=512, verbose_name="Razão Social"),
                ),
                ("cnpj", models.CharField(max_length=25, verbose_name="C.N.P.J.")),
            ],
        ),
        migrations.CreateModel(
            name="Unidade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=212)),
                (
                    "empresa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="unidades",
                        to="clientes.empresa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=112)),
                ("telefone", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "cpf",
                    models.CharField(
                        blank=True, max_length=25, null=True, verbose_name="C.P.F."
                    ),
                ),
                (
                    "empresa",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="clientes.empresa",
                    ),
                ),
                (
                    "endereco",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="enderecos.endereco",
                        verbose_name="Endereço",
                    ),
                ),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuário",
                    ),
                ),
            ],
        ),
    ]