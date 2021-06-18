from django.contrib import admin
from django.urls import path
from src.core_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', views.CreateUpdate.as_view(), name="index"),
    path('polygon/<id>', views.CreateUpdate.as_view(), name="polygon"),
    path('', views.PolygonList.as_view(), name="list"),
]
