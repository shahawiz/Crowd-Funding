# Generated by Django 2.1.5 on 2019-02-22 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20190222_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_images',
            name='project_img',
            field=models.ImageField(blank=True, default='projects_pics/nopic.jpeg', upload_to='multi'),
        ),
    ]
