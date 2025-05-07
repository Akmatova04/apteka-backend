# apteka_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    medicine_list_view, medicine_detail_view,
    create_order_view, order_success_view,
    signup_view, about_us_view, contact_us_view # Жаңы view'ларды импорттоо
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # Сайттын баракчалары
    path('', medicine_list_view, name='home'),
    path('medicines/', medicine_list_view, name='medicine-list-page'),
    path('medicines/<int:pk>/', medicine_detail_view, name='medicine-detail-page'),

    # Буйрутма процесси
    path('create-order/', create_order_view, name='create-order-page'),
    path('order-success/<int:order_id>/', order_success_view, name='order-success-page'),

    # "Биз жөнүндө" жана "Байланыш" баракчалары
    path('about-us/', about_us_view, name='about-us-page'),
    path('contact-us/', contact_us_view, name='contact-us-page'),

    # Аутентификация
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')), # login, logout, password_reset ж.б.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)