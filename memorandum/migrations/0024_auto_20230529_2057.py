# Generated by Django 3.2.9 on 2023-05-30 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memorandum', '0023_alter_menorandum_date_expiring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivos',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='menorandum',
            name='archivos',
            field=models.ManyToManyField(blank=True, to='memorandum.Archivos'),
        ),
    ]