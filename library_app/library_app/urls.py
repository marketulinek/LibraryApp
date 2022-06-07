from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ils.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = 'ils.views.custom_error_404'
handler500 = 'ils.views.custom_error_500'
handler403 = 'ils.views.custom_error_403'
handler400 = 'ils.views.custom_error_400'