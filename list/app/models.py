from django.db import models
from django.contrib.auth.models import User
# تصنيف العناصر في القائمة
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# حالة العنصر في قائمة التسوق
class Item(models.Model):

    name = models.CharField(max_length=255)  # اسم العنصر
    quantity = models.CharField(max_length=255)  # الكمية (مثال: 2 kg)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # تصنيف العنصر
    status = models.CharField(max_length=20, default='Not Purchased')  # حالة العنصر
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.quantity})"
