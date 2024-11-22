from django import forms
from .models import Client, Product, OrderItem, Order
from django.forms import inlineformset_factory


# форма создания нового клиента
class ClientForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Имя",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "example@example.com"}
        ),
    )
    phone = forms.CharField(
        max_length=16,
        label="Телефон",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7(999)999-99-99 "}
        ),
    )
    address = forms.CharField(
        max_length=100,
        label="Адрес",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите адрес"}
        ),
    )


# форма создания нового товара
class ProductForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Название товара",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите название товара"}
        ),
    )
    description = forms.CharField(
        label="Описание товара",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Введите описание товара"}
        ),
    )
    price = forms.DecimalField(
        label="Цена товара",
        max_digits=11,
        decimal_places=2,
        initial=0,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Введите цену"}
        ),
    )
    quantity = forms.IntegerField(
        label="Количество товара",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    product_image = forms.ImageField(
        label="Изображение товара",
        widget=forms.FileInput(attrs={"class": "form-control", "type": "file"}),
    )


# доп класс для обработки товара и его количества
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
        labels = {"product": "Товар", "quantity": "Количество товара"}
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }


# форма создания нового заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["buyer"]
        labels = {"buyer": "Покупатель"}
        widgets = {
            "buyer": forms.Select(attrs={"class": "form-control"}),
        }

    OrderItemFormSet = inlineformset_factory(
        Order, OrderItem, form=OrderItemForm, extra=3
    )
