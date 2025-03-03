from django.db import models

# Create your models here.
# myapp/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Fix 3 (part2): Broken Access Control
    # is_public = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    