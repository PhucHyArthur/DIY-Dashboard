from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from suppliers.models import Suppliers
from warehouse.models import Location
from django.utils.timezone import now
from cloudinary.models import CloudinaryField

class RawMaterials(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    total_quantity = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(_("Is Available"), default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Raw Material")
        verbose_name_plural = _("Raw Materials")

    def update_total_amount(self):
        self.total_amount = sum(line.line_total for line in self.raw_materials_lines.all())
        self.save()

    def update_total_quantity(self):
        self.total_quantity = sum(line.quantity for line in self.raw_materials_lines.all())
        self.save()

class RawMaterialsLine(models.Model):
    raw_material = models.ForeignKey(
        RawMaterials, 
        on_delete=models.CASCADE, 
        related_name="raw_materials_lines", 
        blank=True, 
        null=True
    )
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    supplier = models.ForeignKey(
        Suppliers, 
        on_delete=models.CASCADE, 
        related_name="raw_materials_lines", 
        blank=True, 
        null=True
    )
    location = models.ForeignKey(
        Location, 
        on_delete=models.CASCADE, 
        related_name="raw_materials_lines", 
        blank=True, 
        null=True
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_available = models.BooleanField(_("Is Available"), default=True)

    def save(self, *args, **kwargs):
        if self.quantity and self.price_per_unit:
            self.line_total = self.quantity * self.price_per_unit
        super(RawMaterialsLine, self).save(*args, **kwargs)
        if self.raw_material:
            self.raw_material.update_total_amount()
            self.raw_material.update_total_quantity()

    def __str__(self):
        return f"Line for Raw Material {self.raw_material.name if self.raw_material else 'None'}"


class FinishedProducts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    total_quantity = models.IntegerField(default=0)
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
