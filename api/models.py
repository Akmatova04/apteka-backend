from django.db import models
from django.utils import timezone

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Акча үчүн DecimalField жакшы
    quantity = models.PositiveIntegerField(default=0)


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='medicine_images/', blank=True, null=True) # ЖАҢЫ САТЫП

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None 

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Жаңы', 'Жаңы'),
        ('Иштетүүдө', 'Иштетүүдө'),
        ('Жолдо', 'Жолдо'),
        ('Жеткирилди', 'Жеткирилди'),
        ('Аткарылбады', 'Аткарылбады'),
    ]
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Жаңы')

    def __str__(self):
        return f"Буйрутма #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT) # Дары өчсө, буйрутмада калсын
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2) # Буйрутма учурундагы баа

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name} (Буйрутма: {self.order.id})"

    def save(self, *args, **kwargs):
        # Эгер жаңы түзүлүп жатса, учурдагы бааны сактайбыз
        if not self.pk and self.medicine: # pk = primary key
             self.price_at_order = self.medicine.price
        super().save(*args, **kwargs)