# Generated by Django 4.2.20 on 2025-05-07 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0016_setting_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('book_id', models.CharField(blank=True, max_length=50, null=True)),
                ('fine_amount', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='accession_no',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='setting',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logo'),
        ),
    ]
