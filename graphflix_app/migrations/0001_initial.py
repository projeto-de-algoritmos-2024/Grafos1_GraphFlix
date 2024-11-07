# Generated by Django 5.1.2 on 2024-11-07 02:53

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_genero', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('dtLancamento', models.DateField()),
                ('classificacao', models.CharField(max_length=5)),
                ('posterPath', models.CharField(blank=True, max_length=100)),
                ('backdropPath', models.CharField(blank=True, max_length=100)),
                ('sinopse', models.CharField(blank=True, max_length=500)),
                ('avaliacao', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('notaMinima', models.FloatField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Prefere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='graphflix_app.genero')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id_serie', models.IntegerField(primary_key=True, serialize=False)),
                ('qtd_temporadas', models.IntegerField()),
                ('criador', models.CharField(max_length=50)),
                ('situacao', models.CharField(max_length=15)),
                ('titulo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='graphflix_app.titulo')),
            ],
        ),
        migrations.CreateModel(
            name='Possui',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='graphflix_app.genero')),
                ('titulo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='graphflix_app.titulo')),
            ],
        ),
        migrations.CreateModel(
            name='Filme',
            fields=[
                ('id_filme', models.IntegerField(primary_key=True, serialize=False)),
                ('duracao', models.CharField(max_length=10)),
                ('diretor', models.CharField(max_length=50)),
                ('titulo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='graphflix_app.titulo')),
            ],
        ),
        migrations.CreateModel(
            name='Favorita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('titulo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='graphflix_app.titulo')),
            ],
        ),
        migrations.CreateModel(
            name='Elenco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elenco', models.CharField(max_length=50)),
                ('titulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphflix_app.titulo')),
            ],
        ),
    ]
