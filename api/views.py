# api/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Пагинация үчүн

from .models import Medicine, Order, OrderItem, Category # Category'ни импорттоо
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MedicineSerializer, OrderSerializer
from .forms import SignUpForm

# --- API Views (өзгөрүүсүз калтырабыз, эгер керек болсо, аларды да жазам) ---
class MedicineListCreateView(generics.ListCreateAPIView): # ... мурункудай ...
    queryset = Medicine.objects.all().order_by('name')
    serializer_class = MedicineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView): # ... мурункудай ...
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    lookup_field = 'pk'

class OrderListCreateView(generics.ListCreateAPIView): # ... мурункудай ...
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-created_at')
    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

class OrderDetailView(generics.RetrieveUpdateAPIView): # ... мурункудай ...
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

@api_view(['PUT']) # ... мурункудай ...
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Буйрутма табылган жок'}, status=status.HTTP_404_NOT_FOUND)
    new_status = request.data.get('status')
    if not new_status:
        return Response({'error': 'Жаңы статус берилген жок'}, status=status.HTTP_400_BAD_REQUEST)
    allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
    if new_status not in allowed_statuses:
         return Response(
            {'error': f"Статус '{new_status}' туура эмес. Мүмкүн болгон статустар: {', '.join(allowed_statuses)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    order.status = new_status
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)


# --- Сайттын баракчалары үчүн ФУНКЦИЯЛЫК VIEWS ---

def medicine_list_view(request):
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', None)
    sort_by = request.GET.get('sort', 'name') # Демейки сорттоо - аты боюнча

    all_medicines = Medicine.objects.filter(quantity__gt=0) # Кампадан түгөнбөгөндөрдү гана
    categories = Category.objects.all()
    featured_medicines = Medicine.objects.filter(is_featured=True, quantity__gt=0).order_by('?')[:6] # 6 сунушталган товар
    current_category = None
    page_title = 'Бардык Дарылар'

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        all_medicines = all_medicines.filter(category=current_category)
        page_title = f"{current_category.name} категориясы"

    if search_query:
        all_medicines = all_medicines.filter(name__icontains=search_query)
        title_prefix = f'"{search_query}" боюнча издөө'
        if current_category:
            page_title = f'{title_prefix} ({current_category.name})'
        else:
            page_title = title_prefix
            
    # Сорттоо
    if sort_by == 'price_asc':
        all_medicines = all_medicines.order_by('price')
    elif sort_by == 'price_desc':
        all_medicines = all_medicines.order_by('-price')
    elif sort_by == 'name_desc':
        all_medicines = all_medicines.order_by('-name')
    else: # name_asc же демейки
        all_medicines = all_medicines.order_by('name')


    # Пагинация
    paginator = Paginator(all_medicines, 12) # Бир бетте 12 дары
    page_number = request.GET.get('page')
    try:
        medicines_page = paginator.page(page_number)
    except PageNotAnInteger:
        medicines_page = paginator.page(1)
    except EmptyPage:
        medicines_page = paginator.page(paginator.num_pages)
        
    context = {
        'medicines_page': medicines_page, # Пагинацияланган объектти шаблонго беребиз
        'categories': categories,
        'featured_medicines': featured_medicines,
        'current_category': current_category,
        'page_title': page_title,
        'search_query': search_query,
        'current_sort': sort_by,
    }
    return render(request, 'medicine_list.html', context)

def medicine_detail_view(request, pk): # ... мурункудай ...
    medicine = get_object_or_404(Medicine, id=pk)
    related_medicines = Medicine.objects.filter(category=medicine.category).exclude(id=pk).order_by('?')[:4] if medicine.category else None
    context = {
        'medicine': medicine,
        'page_title': medicine.name,
        'related_medicines': related_medicines
    }
    return render(request, 'medicine_detail.html', context)

def create_order_view(request): # ... мурункудай ...
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        medicine_id = request.POST.get('medicine_id')
        quantity_str = request.POST.get('quantity')
        if not all([customer_name, medicine_id, quantity_str]):
            messages.error(request, "Сураныч, бардык керектүү талааларды толтуруңуз!")
            if medicine_id: return redirect(reverse('medicine-detail-page', kwargs={'pk': medicine_id}))
            return redirect('home')
        try:
            quantity = int(quantity_str)
            medicine = Medicine.objects.get(id=medicine_id)
            if quantity <= 0:
                messages.error(request, "Дарынын саны 0дөн чоң болушу керек.")
                return redirect(reverse('medicine-detail-page', kwargs={'pk': medicine_id}))
            if medicine.quantity < quantity:
                messages.error(request, f"'{medicine.name}' дарысынан жетишсиз. Калдыгы: {medicine.quantity}. Суралган сан: {quantity}.")
                return redirect(reverse('medicine-detail-page', kwargs={'pk': medicine_id}))
            with transaction.atomic():
                order = Order.objects.create(customer_name=customer_name, customer_phone=customer_phone)
                OrderItem.objects.create(order=order, medicine=medicine, quantity=quantity, price_at_order=medicine.price)
                order.total_price = medicine.price * quantity
                order.save()
                medicine.quantity -= quantity
                medicine.save()
            messages.success(request, f"Сиздин буйрутмаңыз (№{order.id}) ийгиликтүү түзүлдү!")
            return redirect(reverse('order-success-page', kwargs={'order_id': order.id}))
        except Medicine.DoesNotExist:
            messages.error(request, "Көрсөтүлгөн дары табылган жок.")
            return redirect('home')
        except ValueError:
            messages.error(request, "Дарынын саны туура сан форматында болушу керек.")
            if medicine_id: return redirect(reverse('medicine-detail-page', kwargs={'pk': medicine_id}))
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Буйрутма түзүүдө күтүлбөгөн ката кетти: {str(e)}")
            if medicine_id: return redirect(reverse('medicine-detail-page', kwargs={'pk': medicine_id}))
            return redirect('home')
    else:
        return redirect('home')

def order_success_view(request, order_id): # ... мурункудай ...
    order = get_object_or_404(Order, id=order_id)
    context = { 'order': order, 'page_title': f"Буйрутма №{order.id} Ийгиликтүү" }
    return render(request, 'order_success.html', context)

def signup_view(request): # ... мурункудай ...
    if request.user.is_authenticated:
        messages.info(request, "Сиз мурунтан эле киргенсиз.")
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Кош келиңиз, {user.username}! Сиз ийгиликтүү катталдыңыз.")
            return redirect('home')
        else:
            messages.error(request, "Каттоо учурунда каталар кетти. Сураныч, маалыматты текшериңиз.")
    else:
        form = SignUpForm()
    context = { 'form': form, 'page_title': 'Катталуу' }
    return render(request, 'registration/signup.html', context)

def about_us_view(request): # ... мурункудай ...
    context = { 'page_title': 'Биз жөнүндө' }
    return render(request, 'about_us.html', context)

def contact_us_view(request): # ... мурункудай ...
    context = { 'page_title': 'Байланыш' }
    return render(request, 'contact_us.html', context)