# Generated by Django 2.2.4 on 2019-08-26 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20190826_1538'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useradminproxy',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자 목록'},
        ),
    ]
