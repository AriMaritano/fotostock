from django.urls import path
from . import views

urlpatterns = [
    path("results", views.show_results, name="results"),
    path("files", views.show_files, name="results"),
    path("fotostock", views.fotostock, name="fotostock"),
    path("", views.fotostock, name="fotostock"),
    path("stock", views.ver_stock, name="stock")
]