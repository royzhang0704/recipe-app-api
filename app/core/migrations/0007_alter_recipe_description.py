# Generated by Django 5.1.1 on 2025-02-26 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
