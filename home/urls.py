from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("ai/", views.ai, name = "ai"),
    path("search/", views.search_database, name = "search"),
    path("database/", views.database, name = "database"),
    path("save_pdf/", views.save_pdf, name = "save_pdf"),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path('pdfs/<int:pdf_id>/download/', views.download_pdf, name='download_pdf'),
]