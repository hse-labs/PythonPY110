from django.urls import path
import app_htmx.views as views


urlpatterns = [
    path('', views.hx_swap_view, name="hx_swap_view"),
    path("inner/", views.swap_inner, name="swap-inner"),
    path("outer/", views.swap_outer, name="swap-outer"),
    path("text/", views.swap_text, name="swap-text"),
    path("before/", views.swap_before, name="swap-before"),
    path("after-begin/", views.swap_after_begin, name="swap-after-begin"),
    path("before-end/", views.swap_before_end, name="swap-before-end"),
    path("after/", views.swap_after, name="swap-after"),
    path("delete/", views.swap_delete, name="swap-delete"),
    path("none/", views.swap_none, name="swap-none"),
]
