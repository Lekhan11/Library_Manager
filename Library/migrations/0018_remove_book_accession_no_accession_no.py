# Generated by Django 4.2.20 on 2025-05-08 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0017_fine_book_accession_no_alter_setting_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='accession_no',
        ),
        migrations.CreateModel(
            name='Accession_No',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession_no', models.CharField(max_length=20, unique=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accession_no', to='Library.book')),
            ],
        ),
    ]
