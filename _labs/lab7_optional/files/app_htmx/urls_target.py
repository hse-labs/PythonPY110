from django.urls import path
import app_htmx.views as views


urlpatterns = [
    path("", views.hx_target_view, name="hx_target_view"),
    path("load-status/", views.load_status, name="load_status"),
    path("row-details/", views.row_details, name="row_details"),
    path("product-details/", views.product_details, name="product_details"),
    path("more-info/", views.more_info, name="more_info"),
    path("validate/", views.validate_email, name="validate_email"),
    path("result/", views.get_result, name="get_result"),
    path("note/", views.show_note, name="show_note"),
]
