from django.contrib import admin
from .models import Medicine, Order, OrderItem

class OrderItemInline(admin.TabularInline): # Буйрутманы көргөндө дарыларын да көрсөтөт
    model = OrderItem
    extra = 1 # Канча бош форма көрсөтүлөт
    readonly_fields = ('price_at_order',) # Бул талааны админкада өзгөртүүгө болбойт

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone')
    inlines = [OrderItemInline] # Жогоруда аныкталган OrderItemInline'ды кошобуз

    def save_model(self, request, obj, form, change):
        # Бул жерге жалпы сумманы кайра эсептөө логикасын кошсо болот,
        # бирок азыр жөнөкөй калтыралы, себеби OrderItem өзүнчө кошулат.
        # Негизгиси, total_price API аркылуу туура эсептелиши керек.
        super().save_model(request, obj, form, change)

@admin.register(OrderItem) # Өзүнчө да көрсөтсө болот, бирок Order ичинде ыңгайлуураак
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'medicine', 'quantity', 'price_at_order')
    readonly_fields = ('price_at_order',)