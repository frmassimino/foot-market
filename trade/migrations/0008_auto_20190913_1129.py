# Generated by Django 2.2.5 on 2019-09-13 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0007_auto_20190913_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ask',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='player.Player'),
        ),
    ]