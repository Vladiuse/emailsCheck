from django.urls import path, include
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.emails, name='emails'),
    path('email_pack/', views.email_pack_list, name='email_pack_list'),
    path('email_pack/<int:email_pack_id>/', views.email_pack, name='email_pack'),
    path('email/<str:email_login>', views.email, name='email'),
    path('email/send_by_date/', views.emails_send_by, name='emails_send_by'),
    path('email/send_by_date/<str:date>/', views.emails_send_by_date, name='emails_send_by_date'),
    path('mail_html/<int:mail_id>', views.mail, name='mail'),
    path('alien_links/', views.alien_links, name='alien_links'),

    ####
    path('test/', views.test, name='test'),
]