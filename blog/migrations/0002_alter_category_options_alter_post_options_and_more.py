# Generated by Django 4.2.2 on 2023-07-07 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('title',)},
        ),
    ]
