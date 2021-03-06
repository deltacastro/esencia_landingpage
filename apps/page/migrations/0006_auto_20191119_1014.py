# Generated by Django 2.2.4 on 2019-11-19 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_eventos_lugar'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventos',
            name='hora',
            field=models.TimeField(default='00:00', verbose_name='Hora'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='fecha',
            field=models.DateField(verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='lugar',
            field=models.CharField(default='', max_length=50, verbose_name='Lugar'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='titulo',
            field=models.CharField(max_length=100, verbose_name='Título'),
        ),
    ]
