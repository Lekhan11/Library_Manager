# Generated by Django 4.2.20 on 2025-03-26 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0004_alter_book_availability_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='edition',
        ),
    ]
