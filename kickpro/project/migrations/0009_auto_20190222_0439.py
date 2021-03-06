# Generated by Django 2.1.5 on 2019-02-22 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20190222_0402'),
    ]

    operations = [
        migrations.CreateModel(
            name='commentReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('subject', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.UserProfileInfo')),
            ],
        ),
        migrations.CreateModel(
            name='projectReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('subject', models.CharField(max_length=100)),
                ('details', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='details',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='projectreport',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project'),
        ),
        migrations.AddField(
            model_name='projectreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.UserProfileInfo'),
        ),
    ]
