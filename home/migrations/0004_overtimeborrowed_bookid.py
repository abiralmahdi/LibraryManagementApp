# Generated by Django 3.0.8 on 2020-12-07 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_borrowedbooks_bookid'),
    ]

    operations = [
        migrations.AddField(
            model_name='overtimeborrowed',
            name='bookID',
            field=models.CharField(default='', max_length=100),
        ),
    ]
