# Generated by Django 5.1.1 on 2024-10-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_prices_recipe_price_rename_tag_recipe_tags_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]