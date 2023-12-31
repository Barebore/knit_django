# Generated by Django 4.2 on 2023-05-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(upload_to='media_knowledge/'),
        ),
    ]
