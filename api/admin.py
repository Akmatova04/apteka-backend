# api/admin.py
from django.contrib import admin
from .models import Medicine, Order, OrderItem, Category # Category'ни импорттоо
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'medicine_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # Слагты автоматтык түрдө толтуруу

    def medicine_count(self, obj):
        return obj.medicines.count()
    medicine_count.short_description = 'Дарылардын саны'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_order',)
    autocomplete_fields = ['medicine']
    min_num = 1

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'is_featured', 'display_image_thumbnail')
    list_filter = ('category', 'is_featured', 'quantity')
    search_fields = ('name', 'description')
    list_editable = ('price', 'quantity', 'is_featured') # Тизмеден түз өзгөртүү
    autocomplete_fields = ['category'] # Категорияны тандоону жеңилдетүү

    def display_image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: auto;" />', obj.image.url)
        return "(Сүрөт жок)"
    display_image_thumbnail.short_description = 'Сүрөтү'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price_display', 'status', 'created_at_formatted')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('total_price', 'created_at')
    date_hierarchy = 'created_at'

    def total_price_display(self, obj):
        return f"{obj.total_price} сом"
    total_price_display.short_description = 'Жалпы баасы'

    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")
    created_at_formatted.short_description = 'Түзүлгөн күнү'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_link', 'medicine_link', 'quantity', 'price_at_order', 'total_item_price_display')
    list_select_related = ('order', 'medicine')
    search_fields = ('order__customer_name', 'order__id', 'medicine__name')
    readonly_fields = ('price_at_order',)
    list_filter = ('medicine__category', 'medicine') # Категория боюнча да фильтрлөө

    def order_link(self, obj):
        from django.urls import reverse
        link = reverse("admin:api_order_change", args=[obj.order.id])
        return format_html('<a href="{}">Буйрутма #{}</a>', link, obj.order.id)
    order_link.short_description = 'Буйрутма'

    def medicine_link(self, obj):
        if obj.medicine:
            link = reverse("admin:api_medicine_change", args=[obj.medicine.id])
            return format_html('<a href="{}">{}</a>', link, obj.medicine.name)
        return "Дары жок"
    medicine_link.short_description = 'Дары'

    def total_item_price_display(self, obj):
        return f"{obj.get_total_item_price()} сом"
    total_item_price_display.short_description = 'Элементтин суммасы'