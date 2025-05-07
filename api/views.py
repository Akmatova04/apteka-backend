from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view # Функция негизиндеги көрүнүштөр үчүн
from .models import Medicine, Order, OrderItem
from .serializers import MedicineSerializer, OrderSerializer

# --- Дарылар үчүн Views ---
class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    lookup_field = 'pk' # URL'ден ID'ни алуу үчүн (мис: /api/medicines/1/)

# --- Буйрутмалар үчүн Views ---
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.order_by('-created_at') # Акыркылары биринчи
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateAPIView): # Буйрутманы өчүрүүгө азырынча жол бербейбиз
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

# Буйрутманын статусун өзүнчө өзгөртүү үчүн (жөнөкөйүрөөк)
@api_view(['PUT'])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Буйрутма табылган жок'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if not new_status:
        return Response({'error': 'Жаңы статус берилген жок'}, status=status.HTTP_400_BAD_REQUEST)

    # Моделдеги choices менен салыштыруу
    allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if new_status not in allowed_statuses:
         return Response(
            {'error': f"Статус '{new_status}' туура эмес. Мүмкүн болгон статустар: {', '.join(allowed_statuses)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.status = new_status
    order.save()
    serializer = OrderSerializer(order) # Жаңыртылган буйрутманы кайтаруу
    return Response(serializer.data)