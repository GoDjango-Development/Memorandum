# Generated by Django 3.2.9 on 2023-05-26 04:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memorandum', '0017_auto_20230519_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destinatarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nombre_memo', models.CharField(max_length=200, null=True, verbose_name='Nombre del Memorandum')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('remitente', models.CharField(max_length=200, verbose_name='Remitente')),
                ('destinatarios', models.ManyToManyField(to='memorandum.Destinatarios')),
            ],
        ),
    ]
