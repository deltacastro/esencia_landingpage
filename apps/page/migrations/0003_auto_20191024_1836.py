# Generated by Django 2.2.4 on 2019-10-24 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20191024_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
