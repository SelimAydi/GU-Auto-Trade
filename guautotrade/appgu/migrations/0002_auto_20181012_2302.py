# Generated by Django 2.0 on 2018-10-12 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appgu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapdealers',
            name='city',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapdealers',
            name='state',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mapdealers',
            name='zip',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
