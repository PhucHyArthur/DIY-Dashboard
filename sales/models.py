from django.db import models
from django.contrib.auth.models import User
from inventory.models import FinishedProducts
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Cart of {self.user.username}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

class Cart_Line(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_lines")
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


class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Favorites of {self.user.username}"

    class Meta:
        verbose_name = "Favorites"
        verbose_name_plural = "Favorites"


class Favorite_Line(models.Model):
    favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE, related_name="favorite_lines")
    product = models.ForeignKey(FinishedProducts, on_delete=models.CASCADE)  
    added_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.product.name} - Added at {self.added_at}"

    class Meta:
        verbose_name = "Favorite Line"
        verbose_name_plural = "Favorite Lines"
