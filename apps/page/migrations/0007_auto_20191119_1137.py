# Generated by Django 2.2.4 on 2019-11-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0006_auto_20191119_1014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventos',
            options={'ordering': ['fecha', 'hora']},
        ),
        migrations.AlterField(
            model_name='eventos',
            name='hora',
            field=models.TimeField(verbose_name='Hora'),
        ),
    ]
