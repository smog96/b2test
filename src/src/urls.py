from django.contrib import admin
from django.urls import path
from src.core_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name="index"),
    path('<id>', views.Index.as_view(), name="index"),
]
