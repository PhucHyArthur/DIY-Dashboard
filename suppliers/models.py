from django.db import models

class Representative(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tel = models.CharField(max_length=15) 
    email = models.EmailField(max_length=255)
    position = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    bank_branch = models.CharField(max_length=255)
    bank_number = models.CharField(max_length=50) 
    swift_code = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    representative = models.ForeignKey(
        Representative, on_delete=models.SET_NULL, null=True, blank=True, related_name='suppliers'
    )
    avatar = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    tel = models.CharField(max_length=15) 
    email = models.EmailField(max_length=255)
    tax_code = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    bank_branch = models.CharField(max_length=255)
    bank_number = models.CharField(max_length=50) 
    swift_code = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
