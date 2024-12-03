from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("ai/", views.ai, name = "ai"),
    path("search/", views.search_database, name = "search"),
    path("database/", views.database, name = "database"),

    # ACTS CATEGORIZATION
    path("bns/", views.bns, name = "bns"),
    path("ipc/", views.ipc, name = "ipc"),
    path("crpc/", views.crpc, name = "crpc"),
    path("mva/", views.mva, name = "mva"),
    path("cpc/", views.cpc, name = "cpc"),
    path("iea/", views.iea, name = "iea"),

    path("save_pdf/", views.save_pdf, name = "save_pdf"),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path('pdfs/<int:pdf_id>/download/', views.download_pdf, name='download_pdf'),
]