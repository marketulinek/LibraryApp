# Generated by Django 4.0.3 on 2022-06-12 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0007_alter_book_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.IntegerField(default=2000, max_length=4),
        ),
    ]
