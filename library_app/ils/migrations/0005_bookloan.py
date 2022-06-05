# Generated by Django 4.0.3 on 2022-06-05 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ils', '0004_bookreservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('returned_at', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ils.book')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ils.reader')),
            ],
        ),
    ]
