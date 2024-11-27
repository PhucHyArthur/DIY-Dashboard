from django.db import models
from inventory.models import FinishedProducts
from users.models import Employee
from django.conf import settings

class Cart_Line(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(FinishedProducts, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField() 
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) 
    line_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  

    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"

    class Meta:
        verbose_name = "Cart Line"
        verbose_name_plural = "Cart Lines"

class Favorite_Line(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    product = models.ForeignKey(FinishedProducts, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.product.name} - Added at {self.added_at}"

    class Meta:
        verbose_name = "Favorite Line"
        verbose_name_plural = "Favorite Lines"
