# Generated by Django 4.2.20 on 2025-05-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0022_alter_issuedbooks_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
