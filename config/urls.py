from django.contrib import admin
from django.urls import path

from config.api.exchange_rates import btc_usd, history, home
from config.api.tickets import get_all_tickets

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home),
    # Exchange rates
    path("btc_usd/", btc_usd),
    path("history/", history),
    # Tickets
    path("history/", get_all_tickets),
]
