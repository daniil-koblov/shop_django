from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    # адрес для просмотра всех заказов клиента
    path("orders/<int:client_id>", views.orders, name="orders"),
    # адрес для просмотра всех заказов
    path("orders/", views.orders, name="all_orders"),
    # адрес для создания нового клиента
    path("add_client/", views.add_client, name="add_client"),
    # адрес для создания нового товара
    path("add_product/", views.add_product, name="add_product"),
    # адрес для создания нового заказа
    path("add_order/", views.add_order, name="add_order"),
]
