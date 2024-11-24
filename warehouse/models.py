from django.db import models
from django.utils.translation import gettext_lazy as _

class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_fulled = models.BooleanField(_("Is Fulled"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="zones")
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_fulled = models.BooleanField(_("Is Fulled"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Zone")
        verbose_name_plural = _("Zones")


class Aisle(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="aisles")
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_fulled = models.BooleanField(_("Is Fulled"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Aisle")
        verbose_name_plural = _("Aisles")


class Rack(models.Model):
    id = models.AutoField(primary_key=True)
    aisle = models.ForeignKey(Aisle, on_delete=models.CASCADE, related_name="racks")
    name = models.CharField(max_length=255)
    capacity = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_fulled = models.BooleanField(_("Is Fulled"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Rack")
        verbose_name_plural = _("Racks")


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="locations")
    bin_number = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    is_fulled = models.BooleanField(_("Is Fulled"), default=False)

    def __str__(self):
        return self.bin_number

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
