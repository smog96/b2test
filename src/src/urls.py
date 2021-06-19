from django.contrib import admin
from django.urls import path
from src.core_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', views.PolygonViewBase.as_view(), name="create"),
    path('polygon/<id>', views.PolygonView.as_view(), name="polygon"),
    path('manager/', views.PolygonPostView.as_view(), name="polygon_manager"),
    path('', views.PolygonList.as_view(), name="list"),
]
