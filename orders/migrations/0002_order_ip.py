# Generated by Django 3.1 on 2023-07-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ip',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
