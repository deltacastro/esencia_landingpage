# Generated by Django 2.2.4 on 2019-11-13 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asesorias_tramites',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='eventos',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='noticias',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='secciones',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveField(
            model_name='secciones',
            name='orientacion',
        ),
    ]