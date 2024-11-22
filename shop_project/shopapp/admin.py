from django.contrib import admin
from .models import Product, Order, Client, OrderItem
from .admin_mixins import ExportAsCSVMixin


admin.site.site_header = 'Мой магазин'
admin.site.site_title = 'Администрирование сайта магазина'
admin.site.index_title = 'Администрирование сайта магазина'

# Дополнителья обработка в панели администратора при работе с покупителем
@admin.action(description="Сменить имя на Secret")
def reset_name(modeladmin, request, queryset):
    queryset.update(name="Secret")


# Дополнителья обработка в панели администратора при работе с заказами
@admin.action(description="Обнулить количество")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "address", "register_date"]
    ordering = ["name", "register_date"]
    list_filter = ["address", "register_date"]
    search_fields = ["name"]
    search_help_text = "Поиск по имени (name)"
    readonly_fields = ["register_date"]
    actions = [reset_name]
    fieldsets = [
        (
            None,
            {
                "classes": ["wide"],  # будет занимать все доступное место на странице
                "fields": ["name"],
            },
        ),
        (
            "Контакты",
            {
                "classes": ["collapse"],  # будет скрыто в раскрывающемся меню
                "fields": ["email", "phone", "address"],
            },
        ),
        (
            "Дата регистрации",
            {
                "fields": ["register_date"],
            },
        ),
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ["title", "price", "quantity", "product_add_date"]
    ordering = ["title", "-price"]
    list_filter = ["price"]
    search_fields = ["title"]
    search_help_text = "Поиск по названию (title)"
    readonly_fields = ["product_add_date"]
    actions = [reset_quantity]
    fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["title", "description"],
            },
        ),
        (
            "Изображение товара",
            {
                "fields": ["product_image"],
            },
        ),
        (
            "Цена и количество",
            {
                "fields": ["price", "quantity"],
            },
        ),
        (
            "Дата поступления товара",
            {
                "fields": ["product_add_date"],
            },
        ),
    ]

# Доп класс для обработки заказа (возможность указать количество товара при заказе)
class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    # доп панель в создании заказа, с выбором товара и указанием количества товара
    inlines = [OrderItemInline]

    list_display = ["buyer", "total_amount", "order_date"]
    ordering = ["-order_date", "-total_amount"]
    list_filter = ["order_date"]
    search_fields = ["buyer"]
    search_help_text = "Поиск по Клиенту (buyer)"
    readonly_fields = ["order_date"]
    actions = ["export_as_csv"]
    fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["buyer"],
            },
        ),
        (
            "Сумма и дата заказа",
            {
                "fields": ["total_amount", "order_date"],
            },
        ),
    ]
