# Generated by Django 4.2.7 on 2023-11-18 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_api', '0004_rename_producto_almacen_idproducto_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'producto', 'verbose_name_plural': 'productos'},
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]