# api/serializers.py
from rest_framework import serializers
from .models import Medicine, Order, OrderItem # Моделдериңизди импорттоо
from django.db import transaction # Транзакция үчүн

# --- Medicine Serializer (Сүрөт жүктөө мүмкүнчүлүгү менен) ---
class MedicineSerializer(serializers.ModelSerializer):
    # Бул талаа сүрөттү жүктөө жана анын URL'ин кайтаруу үчүн колдонулат.
    # 'required=False' жана 'allow_null=True' сүрөт милдеттүү эмес экенин билдирет.
    image = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'description', 'price', 'quantity', 'image']
        # Эгер бардык талааларды камтыгыңыз келсе, '__all__' колдонсоңуз болот,
        # бирок анда 'image' талаасы ImageField катары туура аныкталганына ынаныңыз.
        # fields = '__all__'


# --- OrderItem Serializer (Өзгөрүүсүз, мурункудай) ---
class OrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    # medicine_id POST/PUT сурамдарында дарыны тандоо үчүн колдонулат
    medicine_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'medicine_id', 'medicine_name', 'quantity', 'price_at_order']
        # price_at_order буйрутма түзүлгөндө автоматтык түрдө толтурулат
        read_only_fields = ('price_at_order',)


# --- Order Serializer (Өзгөрүүсүз, мурункудай) ---
class OrderSerializer(serializers.ModelSerializer):
    # 'items' талаасы OrderItemSerializer'ди колдонуп, буйрутмадагы дарыларды көрсөтөт
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_phone', 'total_price', 'created_at', 'status', 'items']
        # total_price жана created_at автоматтык түрдө толтурулат
        read_only_fields = ('total_price', 'created_at')

    def create(self, validated_data):
        # validated_data'дан 'items' тизмесин алып салабыз, анткени аларды өзүнчө иштетебиз
        items_data = validated_data.pop('items')
        if not items_data:
            raise serializers.ValidationError("Буйрутмада эң аз бир дары болушу керек.")

        # Транзакцияны колдонуу менен, эгер бир жерден ката кетсе, баары артка кайтарылат
        with transaction.atomic():
            # Алгач Order объектисин түзөбүз
            order = Order.objects.create(**validated_data)
            current_total_price = 0 # Буйрутманын жалпы баасын эсептөө үчүн

            for item_data in items_data:
                medicine_id = item_data.get('medicine_id')
                quantity = item_data.get('quantity')

                try:
                    medicine = Medicine.objects.get(id=medicine_id)
                except Medicine.DoesNotExist:
                    raise serializers.ValidationError(f"ID={medicine_id} менен дары табылган жок.")

                if medicine.quantity < quantity:
                    raise serializers.ValidationError(
                        f"'{medicine.name}' дарысынан жетишсиз. Калдыгы: {medicine.quantity}, суралды: {quantity}"
                    )

                # Дарынын санын азайтабыз
                medicine.quantity -= quantity
                medicine.save()

                # OrderItem объектисин түзөбүз
                order_item = OrderItem.objects.create(
                    order=order,
                    medicine=medicine,
                    quantity=quantity,
                    price_at_order=medicine.price # Буйрутма учурундагы бааны сактайбыз
                )
                current_total_price += (order_item.price_at_order * order_item.quantity)

            # Буйрутманын жалпы баасын жаңыртып, сактайбыз
            order.total_price = current_total_price
            order.save()
        return order

    def update(self, instance, validated_data):
        
        validated_data.pop('items', None) # 'items' келсе да, аны эске албайбыз

        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.customer_phone = validated_data.get('customer_phone', instance.customer_phone)
        new_status = validated_data.get('status', instance.status)

        # Статустун туура экенин текшерүү (моделдеги choices'тен)
        allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in allowed_statuses:
            raise serializers.ValidationError(
                f"Статус '{new_status}' туура эмес. Мүмкүн болгон статустар: {', '.join(allowed_statuses)}"
            )

        instance.status = new_status
        instance.save()
        return instance