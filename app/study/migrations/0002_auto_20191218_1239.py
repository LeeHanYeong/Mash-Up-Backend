# Generated by Django 2.2.8 on 2019-12-18 03:39

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='study',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='study',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='studymeeting',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='studymeeting',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='studymembership',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='studymembership',
            name='modified_at',
        ),
        migrations.AddField(
            model_name='study',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='studymeeting',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studymeeting',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='studymembership',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studymembership',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
