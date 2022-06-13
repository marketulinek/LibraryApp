# Generated by Django 4.0.3 on 2022-06-13 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0012_alter_book_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookloan',
            name='status_type',
            field=models.CharField(blank=True, choices=[('Borrowed', 'Book borrowed'), ('Completed', 'Book loan completed')], max_length=10, null=True),
        ),
    ]
