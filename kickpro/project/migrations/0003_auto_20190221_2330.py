# Generated by Django 2.1.5 on 2019-02-21 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_main_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='main_pic',
            field=models.ImageField(blank=True, default='profile_pics/nopic.jpeg', upload_to='projects_pics'),
        ),
    ]
