# Generated by Django 2.1.2 on 2018-10-15 19:37

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('dprev_backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='DPrevUser',
        ),
    ]
