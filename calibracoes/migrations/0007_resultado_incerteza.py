# Generated by Django 4.2 on 2023-06-12 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calibracoes", "0006_calibracao_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="resultado",
            name="incerteza",
            field=models.TextField(blank=True, null=True),
        ),
    ]
