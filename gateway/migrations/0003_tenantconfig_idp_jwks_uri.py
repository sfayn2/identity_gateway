# Generated by Django 5.2.4 on 2025-07-23 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0002_rename_idp_metadata_url_tenantconfig_idp_authorization_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantconfig',
            name='idp_jwks_uri',
            field=models.URLField(blank=True, null=True),
        ),
    ]
