# Generated by Django 4.2 on 2023-05-18 11:57

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_library', '0005_alter_testrichtext_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='TinyMCEText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
    ]
