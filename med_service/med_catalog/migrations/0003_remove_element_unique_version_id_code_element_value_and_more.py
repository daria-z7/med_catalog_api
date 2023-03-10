# Generated by Django 4.1 on 2023-01-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_catalog', '0002_rename_element_value_element_value'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='element',
            name='unique_version_id_code_element_value',
        ),
        migrations.AddConstraint(
            model_name='element',
            constraint=models.UniqueConstraint(fields=('version_id', 'code', 'value'), name='unique_version_id_code_value'),
        ),
    ]
