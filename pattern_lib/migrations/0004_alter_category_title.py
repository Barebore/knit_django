# Generated by Django 4.2 on 2023-05-16 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern_lib', '0003_remove_pattern_mini_pattern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
