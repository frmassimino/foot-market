# Generated by Django 2.2.5 on 2019-09-13 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_auto_20190912_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='ask',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='ask',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
