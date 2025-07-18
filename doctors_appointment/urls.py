from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('bookings/', include(('bookings.urls', 'bookings'), namespace='bookings')),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
    path('doctors/', include(('doctors.urls', 'doctor'), namespace='doctor')),
    path('users/', include('users.urls', namespace='users')),
    path('hospitals/', include(('hospitals.urls', 'hospitals'), namespace='hospitals')),
    path('hospital/staff/', include(('hospital_staff.urls', 'hospital_staff'), namespace='hospital_staff')),
    path('patients/', include(('patients.urls', 'patients'), namespace='patients')),  # رابط المرضى
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),  # رابط المراجعات
    path('api/', include('api.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include(('reports.urls', 'reports'), namespace='reports')),  # تقارير
    path('advertisements/', include(('advertisements.urls', 'advertisements'), namespace='advertisements')),

    # صفحة ثابتة لتفاصيل المستشفى
    path('hospital_static.html', TemplateView.as_view(template_name='hospital_static.html'), name='hospital_static'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
