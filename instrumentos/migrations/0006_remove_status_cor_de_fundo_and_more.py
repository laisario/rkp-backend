# Generated by Django 4.2 on 2023-05-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrumentos', '0005_status_cor_de_fundo_status_cor_do_texto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='cor_de_fundo',
        ),
        migrations.RemoveField(
            model_name='status',
            name='cor_do_texto',
        ),
        migrations.AddField(
            model_name='status',
            name='cor',
            field=models.CharField(default='success', max_length=20),
        ),
    ]
