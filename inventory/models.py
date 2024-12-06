from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from warehouse.models import Location
from django.utils.timezone import now
from cloudinary.models import CloudinaryField

class RawMaterials(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    unit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantity_in_stock = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="raw_materials", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    expired_date = models.DateField(_("Expiry Date"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    description = models.TextField(blank=True, null=True)
    expired_date = models.DateField(_("Expiry Date"))
    is_available = models.BooleanField(_("Is Available"), default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Finished Product")
        verbose_name_plural = _("Finished Products")

class Image(models.Model):
    url = CloudinaryField('image')
    raw_material = models.ForeignKey(
        RawMaterials, on_delete=models.CASCADE, related_name='images', blank=True, null=True
    )
    finished_product = models.ForeignKey(
        FinishedProducts, on_delete=models.CASCADE, related_name='images', blank=True, null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
