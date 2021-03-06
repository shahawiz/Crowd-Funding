# Generated by Django 2.1.5 on 2019-02-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20190222_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_project',
            field=models.CharField(choices=[('1', 'Yes'), ('0', 'No')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='project',
            name='main_pic',
            field=models.ImageField(blank=True, default='projects_pics/default.jpg', upload_to='projects_pics'),
        ),
    ]
