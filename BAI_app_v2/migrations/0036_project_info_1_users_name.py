# Generated by Django 3.1.2 on 2020-12-28 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BAI_app_v2', '0035_auto_20201227_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_info_1',
            name='users_name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
