# Generated by Django 2.2.5 on 2019-09-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipo', '0005_auto_20190911_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidder',
            name='value_last',
            field=models.IntegerField(default=0),
        ),
    ]
