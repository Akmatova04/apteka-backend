# api/urls.py
from django.urls import path
from .views import (
    MedicineListCreateView,
    MedicineDetailView,
    OrderListCreateView,
    OrderDetailView,
    update_order_status
    # Эгерде 'home_page_view' api/views.py ичинде болсо, аны да импорттосо болот,
    # бирок ал адатта негизги urls.py үчүн колдонулат.
    # Эгер "dummy_view" дагы эле бар болсо, аны өчүрүп салсаңыз болот, же калтырсаңыз да болот.
)

# Эгерде dummy_view (test үчүн) калган болсо:
# from django.http import HttpResponse
# def dummy_view(request):
# return HttpResponse("API test")

urlpatterns = [
    # Дарылар үчүн жолдор
    path('medicines/', MedicineListCreateView.as_view(), name='medicine-list-create'),
    path('medicines/<int:pk>/', MedicineDetailView.as_view(), name='medicine-detail'),

    # Буйрутмалар үчүн жолдор
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', update_order_status, name='order-status-update'),

    # Эгер "dummy_view" тест үчүн керек болсо, аны калтырсаңыз болот:
    # path('test/', dummy_view, name='test-api'), # Бул сапты өчүрүп салсаңыз болот, эгер кереги жок болсо
]