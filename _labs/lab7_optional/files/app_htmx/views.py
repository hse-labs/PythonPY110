from django.shortcuts import render
from django.http import HttpResponse
import random


def load_products_html(request):  # Возвращаем список продуктов через html
    products = ["Телефон", "Ноутбук", "Наушники", "Клавиатура", "Мышь", "Монитор"]
    html = "".join(f"<li>{product}</li>" for product in random.sample(products,  4))  # Получаем 4 случайных товара из списка и формируем html
    return HttpResponse(html)


def load_products_with_render(request):  # Возвращаем список продуктов через render шаблона list_products.html
    products = ["Телефон", "Ноутбук", "Наушники", "Клавиатура", "Мышь", "Монитор"]
    return render(request, 'app_htmx/list_products.html', {'products': random.sample(products,  4)})


def product_list_view(request):  # Основной шаблон с кнопкой перезагрузки продуктов
    return render(request, 'app_htmx/products.html')
