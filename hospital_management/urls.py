from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from paymentapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('doctor/', include('doctor_app.urls')),
    path('patient/', include('patient_app.urls')),
    path("payment/<pk>", views.order_payment, name="payment"),
    path("callback/<pk>", views.callback, name="callback"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
