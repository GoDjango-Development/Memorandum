# Generated by Django 3.2.9 on 2023-04-14 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorandum', '0015_alter_archivos_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menorandum',
            name='date_expiring',
            field=models.DateField(null=True, verbose_name='Fecha de Expiración'),
        ),
    ]
