# Generated by Django 2.2.10 on 2020-03-11 15:43

from django.db import migrations
from django.db.models.aggregates import Max


def forward(apps, schema_editor):
    from django.apps import apps as django_apps
    from django.contrib.contenttypes.management import create_contenttypes

    app = django_apps.get_app_config("django_auth_adfs_db")
    create_contenttypes(app)

    AppGroup = apps.get_model("admin_index.AppGroup")
    ContentType = apps.get_model("admin_index.ContentTypeProxy")
    ADFSConfig = apps.get_model("django_auth_adfs_db.ADFSConfig")

    max_order = AppGroup.objects.aggregate(max=Max("order"))["max"] or 0
    config, _ = AppGroup.objects.get_or_create(
        slug="configuration", defaults={"name": "Configuratie", "order": max_order + 1,}
    )
    ct = ContentType.objects.get_for_model(ADFSConfig)
    config.models.add(ct)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_initial_admin_index"),
        ("django_auth_adfs_db", "0001_initial"),
    ]

    operations = [migrations.RunPython(forward, migrations.RunPython.noop)]
