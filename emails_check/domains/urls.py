from django.urls import path, include
from . import views

app_name = 'domains'

urlpatterns = [
    path('', views.domains_list, name='domains_list'),
    path('domain/<str:domain_id>/', views.domain, name='domain'),
]