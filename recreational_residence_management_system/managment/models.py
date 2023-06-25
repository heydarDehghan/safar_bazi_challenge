from django.db import models
from django.contrib.auth.models import User


class StandardCapacityDetail(models.Model):
    adult_number = models.IntegerField(default=0)
    child_number = models.IntegerField(default=0)
    baby_number = models.IntegerField(default=0)
    adult_price = models.DecimalField(max_digits=10, decimal_places=2)
    child_price = models.DecimalField(max_digits=10, decimal_places=2)
    baby_price = models.DecimalField(max_digits=10, decimal_places=2)
    standard_capacity = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    create_data = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.standard_capacity = self.adult_number + self.child_number + self.baby_number
        self.total_price = self.adult_number * self.adult_price + self.child_number * self.child_price + self.baby_number * self.baby_price
        super().save(*args, **kwargs)


class ExtraCapacityDetail(models.Model):
    extra_adult_price = models.DecimalField(max_digits=10, decimal_places=2)
    extra_child_price = models.DecimalField(max_digits=10, decimal_places=2)
    extra_baby_price = models.DecimalField(max_digits=10, decimal_places=2)
    create_data = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now=True)


# Define the models for the residence and the pricing
class Residence(models.Model):
    # A model for a residence product that has a name, a description, a standard capacity, and a calendar of prices
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    standard_capacity_detail = models.ForeignKey(StandardCapacityDetail, on_delete=models.CASCADE)
    extra_capacity_detail = models.ForeignKey(ExtraCapacityDetail, on_delete=models.CASCADE)
    create_data = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    PAID = 1
    UNPAID = 2
    PAYMENT_STATUS = [
        (PAID, 'paid'),
        (UNPAID, 'unpaid'),
    ]
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    standard_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(choices=PAYMENT_STATUS, default=UNPAID, max_length=6)
    is_canceled = models.BooleanField(default=False)
    extra_adult_num = models.IntegerField()
    extra_child_num = models.IntegerField()
    extra_baby_num = models.IntegerField()
    create_data = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now=True)


