import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta

from .forms import ClientForm, ProductForm, OrderForm, OrderItem, OrderItemForm
from .models import Order, Client, Product
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory


logger = logging.getLogger(__name__)


def index(request):
    context = {
        "title": "Главная страница",
    }
    logger.info("Index page accessed")
    return render(request, "shopapp/index.html", context)


def about(request):
    context = {
        "title": "О себе",
    }
    logger.info("About page accessed")
    return render(request, "shopapp/about.html", context)


# отображение заказов
def orders(request, client_id: int = None):
    # если передан ID покупателя, отображаем его заказы
    if client_id:
        client = get_object_or_404(Client, id=client_id)
        order = Order.objects.filter(buyer=client)
        today = timezone.now()
        # список обработки количества товара в заказе
        quantities = []
        for ord in order:
            for item in ord.orderitem_set.all():
                quantities.append(item.quantity)

        # Заказы клиента за период времени
        order_week = order.filter(order_date__gte=today - timedelta(days=7))
        order_month = order.filter(order_date__gte=today - timedelta(days=30))
        order_year = order.filter(order_date__gte=today - timedelta(days=365))

        # Получаем уникальные продукты в заказах
        products_week = {
            product for order in order_week for product in order.products.all()
        }
        products_month = {
            product for order in order_month for product in order.products.all()
        }
        products_year = {
            product for order in order_year for product in order.products.all()
        }

        context = {
            "title": f"Список заказов покупателя {client.name}",
            "client": client,
            "order": order,
            'quantities': quantities[::-1],
            "products_week": products_week,
            "products_month": products_month,
            "products_year": products_year,
        }
    # отображаем все заказы в магазине
    else:
        order = Order.objects.all()
        context = {"title": f"Список всех заказов", "order": order}
    return render(request, "shopapp/orders.html", context)


# создаем нового покупателя
def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            Client.objects.create(
                name=form_data["name"],
                email=form_data["email"],
                phone=form_data["phone"],
                address=form_data["address"],
            )
            logger.info(f"Client added")
            return redirect("index")
    else:
        form = ClientForm()
    context = {"title": "Добавить клиента", "form": form}
    return render(request, "shopapp/new_client.html", context)


# создаем новый товар
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                quantity=form.cleaned_data["quantity"],
                product_image=form.cleaned_data["product_image"],
            )
            fs = FileSystemStorage()
            fs.save(product.product_image.name, product.product_image)
            product.save()
            return redirect("index")
    else:
        form = ProductForm()
    context = {"title": "Добавить товар", "form": form}
    return render(request, "shopapp/new_product.html", context)


# обработка создания нового заказа
def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            formset = inlineformset_factory(
                Order, OrderItem, form=OrderItemForm, extra=3
            )
            formset = formset(request.POST, instance=new_order)

            if formset.is_valid():
                new_order.save()
                formset.save()
                new_order.calculate_total()
                return redirect("index")
    else:
        form = OrderForm()
    context = {"title": "Сделать заказ", "form": form}
    return render(request, "shopapp/new_order.html", context)
