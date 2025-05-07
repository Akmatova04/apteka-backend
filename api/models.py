# api/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify # Слаг үчүн

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категориянын аталышы")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Слаг (автоматтык)")
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, verbose_name="Категориянын сүрөтү")
    description = models.TextField(blank=True, null=True, verbose_name="Сүрөттөмөсү")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Кыргызча тамгаларды колдогон жакшыраак слагификация керек болушу мүмкүн
            # Азырынча жөнөкөй slugify колдонобуз
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"
        ordering = ['name']

class Medicine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Дарынын аталышы")
    description = models.TextField(blank=True, null=True, verbose_name="Сүрөттөмөсү")
    category = models.ForeignKey(Category, related_name='medicines', on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name="Категориясы")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баасы (сом)")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Калдыгы (даана)")
    image = models.ImageField(upload_to='medicine_images/', blank=True, null=True, verbose_name="Сүрөтү")
    is_featured = models.BooleanField(default=False, verbose_name="Сунушталган товар") # Карусель үчүн
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Кошулган күнү") # Жаңы келгендер үчүн (милдеттүү эмес)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңыртылган күнү")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Дары"
        verbose_name_plural = "Дарылар"
        ordering = ['name'] # Демейки иреттөө

class Order(models.Model):
    STATUS_CHOICES = [
        ('Жаңы', 'Жаңы'), ('Иштетүүдө', 'Иштетүүдө'), ('Жолдо', 'Жолдо'),
        ('Жеткирилди', 'Жеткирилди'), ('Аткарылбады', 'Аткарылбады'),
    ]
    customer_name = models.CharField(max_length=100, verbose_name="Кардардын аты-жөнү")
    customer_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Кардардын телефону")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Жалпы баасы (сом)")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Түзүлгөн убактысы")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Жаңы', verbose_name="Статусу")

    def __str__(self):
        return f"Буйрутма #{self.id} - {self.customer_name}"

    class Meta:
        verbose_name = "Буйрутма"
        verbose_name_plural = "Буйрутмалар"
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Буйрутма")
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, verbose_name="Дары")
    quantity = models.PositiveIntegerField(verbose_name="Саны")
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Буйрутма учурундагы баасы")

    def __str__(self):
        medicine_name = self.medicine.name if self.medicine else "Өчүрүлгөн дары"
        return f"{self.quantity} x {medicine_name} (Буйрутма: {self.order.id})"
    
    def get_total_item_price(self):
        return self.price_at_order * self.quantity

    class Meta:
        verbose_name = "Буйрутманын элементи"
        verbose_name_plural = "Буйрутманын элементтери"