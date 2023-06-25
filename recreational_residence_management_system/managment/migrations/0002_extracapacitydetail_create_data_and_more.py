# Generated by Django 4.2.2 on 2023-06-25 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("managment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="extracapacitydetail",
            name="create_data",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="extracapacitydetail",
            name="update_data",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="residence",
            name="create_data",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="residence",
            name="update_data",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="standardcapacitydetail",
            name="create_data",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="standardcapacitydetail",
            name="update_data",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="Booking",
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
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[(1, "paid"), (2, "unpaid")], default=2, max_length=6
                    ),
                ),
                ("is_canceled", models.BooleanField(default=False)),
                ("create_data", models.DateTimeField(auto_now_add=True)),
                ("update_data", models.DateTimeField(auto_now=True)),
                (
                    "residence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="managment.residence",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
