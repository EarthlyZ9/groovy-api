# Generated by Django 4.0.2 on 2022-05-16 17:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0005_remove_user_is_deleted_alter_user_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True),
        ),
    ]