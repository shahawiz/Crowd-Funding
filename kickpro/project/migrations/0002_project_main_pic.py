# Generated by Django 2.1.5 on 2019-02-21 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='main_pic',
            field=models.ImageField(blank=True, default='profile_pics/nopic.jpeg', upload_to='project_pics'),
        ),
    ]
