# Generated by Django 2.0.7 on 2018-08-01 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appgu', '0010_auto_20180726_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=5000)),
                ('link', models.CharField(max_length=1000)),
            ],
        ),
    ]
