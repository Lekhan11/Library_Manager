# Generated by Django 5.1.6 on 2025-03-05 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0003_book_category_issuedbooks_reservation_delete_books_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
