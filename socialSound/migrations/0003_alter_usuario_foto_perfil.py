# Generated by Django 5.1.1 on 2024-12-11 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialSound', '0002_alter_detallealbum_album'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='foto_perfil',
            field=models.ImageField(blank=True, default='fotos_perfil/default_profile.png', upload_to='fotos_perfil/'),
        ),
    ]
