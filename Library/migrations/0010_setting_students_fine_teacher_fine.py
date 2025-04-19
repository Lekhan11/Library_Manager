# Generated by Django 4.2.20 on 2025-04-18 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0009_returnedbooks_condition'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maxDueStud', models.IntegerField(default=0)),
                ('maxDueTeach', models.IntegerField(default=0)),
                ('fineStud', models.IntegerField(default=0)),
                ('fineTeach', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='students',
            name='fine',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacher',
            name='fine',
            field=models.IntegerField(default=0),
        ),
    ]
