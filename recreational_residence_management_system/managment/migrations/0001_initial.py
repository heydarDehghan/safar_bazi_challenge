# Generated by Django 4.2.2 on 2023-06-24 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Residence",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StandardCapacityDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("adult_number", models.IntegerField(default=0)),
                ("child_number", models.IntegerField(default=0)),
                ("baby_number", models.IntegerField(default=0)),
                ("adult_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("child_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("baby_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("standard_capacity", models.IntegerField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "residence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="managment.residence",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExtraCapacityDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "extra_adult_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "extra_child_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "extra_baby_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "residence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="managment.residence",
                    ),
                ),
            ],
        ),
    ]
