# payment/models.py
from django.db import models

class Payment(models.Model):
    client_id = models.CharField(max_length=100)  # ID của client
    order_id = models.CharField(max_length=100, unique=True)  # ID của đơn hàng (duy nhất)
    amount = models.IntegerField()
    description = models.TextField()  # Mô tả đơn hàng
    status = models.CharField(max_length=20, default='pending')  # Trạng thái giao dịch
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày tạo giao dịch

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"
