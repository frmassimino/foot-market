# Generated by Django 2.2.5 on 2019-09-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipo', '0006_bidder_value_last'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidder',
            name='value_actual',
            field=models.IntegerField(default=0),
        ),
    ]
