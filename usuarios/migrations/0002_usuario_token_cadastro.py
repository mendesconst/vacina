# Generated by Django 3.2.7 on 2022-06-12 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='token_cadastro',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
