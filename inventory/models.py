from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from warehouse.models import Location

class RawMaterials(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    image = ArrayField(models.URLField(max_length=200), blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    unit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantity_in_stock = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="raw_materials", blank=True, null=True)
    description = models.TextField(max_length=255)
    expired_date = models.DateField(_("Expiry Date"))
    is_available = models.BooleanField(_("Is Available"), default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Raw Material")
        verbose_name_plural = _("Raw Materials")

class FinishedProducts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantity_in_stock = models.IntegerField(default=0)
    unit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="finished_products", blank=True, null=True)
    description = models.TextField(max_length=255)
    expired_date = models.DateField(_("Expiry Date"))
    image = ArrayField(models.TextField(), blank=True, null=True)
    is_available = models.BooleanField(_("Is Available"), default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Finished Product")
        verbose_name_plural = _("Finished Products")
