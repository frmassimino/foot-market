# Generated by Django 2.2.5 on 2019-09-11 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipo', '0003_auto_20190911_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='ipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipo.Ipo'),
        ),
    ]
