from __future__ import unicode_literals

from django.db import models

# Create your models here.
customer_type = (
    ("Active", "Active"),
    ("Inactive", "Inactive")
)


class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(
        max_length=50, null=False, blank=True)
    other_names = models.CharField(max_length=50, default=" ")
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=30, null=False, blank=True)
    balance = models.IntegerField(default="0")
    customer_status = models.CharField(
        max_length=100, choices=customer_type, default="Active")
    address = models.CharField(
        max_length=50, null=False, blank=False)

    def save(self, *args, **kwargs):
        return super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{}:{}".format(self.first_name, self.last_name)
