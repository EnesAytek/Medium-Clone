# Generated by Django 4.2.2 on 2023-07-07 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('created_at',)},
        ),
    ]
