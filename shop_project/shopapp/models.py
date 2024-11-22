from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


# Покупатель
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=100)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, email: {self.email}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


# Товар
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=11, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    product_add_date = models.DateField(auto_now_add=True)
    product_image = models.ImageField(upload_to="product_images/", default=None)

    def __str__(self):
        return f"{self.title}, цена: {self.price}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


# Заказ
class Order(models.Model):
    buyer = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="OrderItem")
    total_amount = models.DecimalField(
        max_digits=64, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Клиент: {self.buyer}, сумма заказа = {self.total_amount}"

    def calculate_total(self):
        total = Decimal(0)
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.product.price * item.quantity
        self.total_amount = total
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


# Доп модель для создания в заказе товара и его количества
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Заказ: {self.order.id}, Товар: {self.product.title}, Количество: {self.quantity}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
