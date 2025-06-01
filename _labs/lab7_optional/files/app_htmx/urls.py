from django.urls import path, include
import app_htmx.views as views

app_name = 'app_htmx'

urlpatterns = [
    path('products/', views.product_list_view, name="products"),
    path('load_products/', views.load_products_html, name="load_products_html"),
    path('load_products/render/', views.load_products_with_render, name="load_products_with_render"),
    path("hx-target/", include('app_htmx.urls_target')),
    path("hx-swap/", include('app_htmx.urls_swap')),
    path("hx-trigger/", include('app_htmx.urls_trigger')),
]
