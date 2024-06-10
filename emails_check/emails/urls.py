from django.urls import path, include
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.emails, name='emails'),
    path('email/<str:email_login>', views.email, name='email'),
    path('mail_html/<int:mail_id>', views.mail_html, name='mail_html'),
    path('alien_links/', views.alien_links, name='alien_links'),
]