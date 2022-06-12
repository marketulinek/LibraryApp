# Generated by Django 4.0.3 on 2022-06-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0006_book_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('Available', 'Book Available'), ('Reserved', 'Book Reserved'), ('Borrowed', 'Book Borrowed'), ('Unavailable', 'Book Unavailable')], default='Available', max_length=20),
        ),
    ]