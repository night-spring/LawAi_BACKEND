from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("ai/", views.ai, name = "ai"),
    path("search/", views.search_database, name = "search"),
    path("data/", views.data, name = "data"),
]