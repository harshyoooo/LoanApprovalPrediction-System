# loan_api_project/urls.py

from django.contrib import admin
from django.urls import path, include
from loan_api_app.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', include('loan_api_app.urls')),
]
