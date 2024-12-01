from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("ai/", views.ai, name = "ai"),
    path("search/", views.search_database, name = "search"),
    path("database/", views.database, name = "database"),
    path("pdf/", views.pdf, name = "pdf"),
    path('serve-pdf/<int:document_id>/', views.serve_pdf, name='serve_pdf'),
]