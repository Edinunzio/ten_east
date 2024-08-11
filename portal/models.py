from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country_of_residence = models.CharField(max_length=100)
    investor_types = models.ManyToManyField('InvestorType', related_name='users')
    def __str__(self):
        return self.username

class Offering(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    media_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    irr = models.FloatField()
    moic = models.FloatField()
    summary = models.TextField()
    minimum = models.IntegerField()
    tags = models.ManyToManyField('OfferingTag', related_name='offerings')
    investor_types = models.ManyToManyField('InvestorType', related_name='offerings')
    is_ai = models.BooleanField(default=False)
    is_qc = models.BooleanField(default=False)
    is_qp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Offering, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class OfferingTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class InvestorType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RequestAllocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_allocations')
    offering = models.ForeignKey('Offering', on_delete=models.CASCADE, related_name='request_allocations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offering.title} - ${self.amount}"