# Generated by Django 3.2.9 on 2023-04-11 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memorandum', '0011_auto_20230411_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivos',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]