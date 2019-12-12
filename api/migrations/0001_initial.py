# Generated by Django 3.0 on 2019-12-11 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ParkingSpot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                ("free", models.BooleanField(default=True)),
            ],
        )
    ]
