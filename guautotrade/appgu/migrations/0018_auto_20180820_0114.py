# Generated by Django 2.0 on 2018-08-19 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appgu', '0017_events_tuscany_newsposts_tuscany_vehicles_tuscany'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicles',
            name='headline_en',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='vehicles',
            name='headline_nl',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]