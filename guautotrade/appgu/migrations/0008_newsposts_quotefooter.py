# Generated by Django 2.0.6 on 2018-07-22 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appgu', '0007_auto_20180722_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsposts',
            name='quotefooter',
            field=models.CharField(default='From X website', max_length=500),
            preserve_default=False,
        ),
    ]