# Generated by Django 5.1.2 on 2024-11-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphflix_app', '0003_alter_titulo_avaliacao_alter_titulo_backdroppath_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filme',
            name='diretor',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='serie',
            name='criador',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
