# Generated by Django 2.2 on 2022-10-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('snumber', models.CharField(max_length=100, verbose_name='snumber')),
                ('logname', models.CharField(max_length=1000)),
            ],
        ),
    ]