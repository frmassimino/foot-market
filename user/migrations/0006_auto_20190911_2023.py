# Generated by Django 2.2.5 on 2019-09-11 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190911_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='player.Player'),
        ),
    ]
