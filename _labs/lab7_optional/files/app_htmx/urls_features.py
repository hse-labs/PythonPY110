from django.urls import path
import app_htmx.views as views

urlpatterns = [
    path('', views.hx_features_view, name='hx_features_view'),
    path('params/', views.params_view, name='hx-params'),
    path('vals/', views.vals_view, name='hx-vals'),
    path('include/', views.include_view, name='hx-include'),
    path('upload/', views.upload_view, name='hx-encoding'),
    path('push-url/', views.push_url_view, name='hx-push-url'),
    path('select/', views.select_view, name='hx-select'),
    path('select-oob/', views.select_oob_view, name='hx-select-oob'),
    path('ext/', views.ext_view, name='hx-ext'),
    path('confirm-delete/', views.confirm_view, name='hx-confirm'),
    path('disable/', views.disable_view, name='hx-disable'),
    path('indicator/', views.indicator_view, name='hx-indicator'),
    path('headers/', views.headers_view, name='hx-headers'),
    path('boost/', views.boost_page, name='hx-boost'),
    path('on/', views.on_event_view, name='hx-on'),
    path('timeout/', views.timeout_view, name='hx-timeout'),
    path('history/', views.history_view, name='hx-history'),
]
