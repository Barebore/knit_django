# Generated by Django 4.2 on 2023-04-25 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pattern_lib', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='scheme_description',
            field=models.ImageField(upload_to='scheme_description_image/'),
        ),
    ]
