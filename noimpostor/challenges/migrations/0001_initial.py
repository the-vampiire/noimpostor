# Generated by Django 2.0.2 on 2018-04-08 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import root.base_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField()),
                ('title', models.CharField(max_length=140)),
                ('notes', models.TextField(blank=True)),
                ('privacy', models.IntegerField(choices=[(-1, 'private'), (0, 'anonymous'), (1, 'public')], default=root.base_models.Privacy(-1), verbose_name='Privacy Setting')),
                ('impostor_level', models.IntegerField(choices=[(0, 'Shadow'), (1, 'Looming'), (2, 'Consumed'), (3, 'Meltdown')], default=0, verbose_name='Panic Level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'challenges',
            },
        ),
        migrations.CreateModel(
            name='Empathy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empathizing_users', to='challenges.Challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empathized_challenges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'empathy',
            },
        ),
    ]
