# Generated by Django 5.1.1 on 2024-10-16 07:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id',
                 models.BigAutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('name',
                 models.CharField(
                     blank=True,
                     max_length=25)),
                ('user',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(
                to='core.tag'),
        ),
    ]
