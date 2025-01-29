from django.urls import path
from . import views
from .views import download_pdf, export_to_excel, export_to_excel1
from .views import chatbot_response
from .views import download_arama_pdf
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [

    path(
        'kullanici_detay/<int:user_id>/',
        user_passes_test(lambda u: u.is_staff)(views.kullanici_detay),
        name='kullanici_detay'
    ),


    path('download-arama-pdf/', download_arama_pdf, name='download_arama_pdf'),
    path('kullanici_raporlar/', views.kullanici_raporlar, name='kullanici_raporlar'),

    path('kullanici_durum_degistir/<int:id>/', views.kullanici_durum_degistir, name='kullanici_durum_degistir'),
    path('kullanicilari_yonet/', views.kullanicilari_yonet, name='kullanicilari_yonet'),
    path('tickets/login/', views.login_view, name='login'),
    
    # Yeni URL Tanımları
    path('yer_sil_yonetim/<int:yer_id>/', views.yer_sil_yonetim, name='yer_sil_yonetim'),
    path('yer_sil_ata/<int:user_id>/<int:yer_id>/', views.yer_sil_ata, name='yer_sil_ata'),

    path('tickets/download_pdf/<int:location_id>/', download_pdf, name='download_pdf'),
    path('tickets/filtered_rapor/<int:location_id>/', views.filtered_rapor, name='filtered_rapor'),
    path('raporlari_yonet/', views.raporlari_yonet, name='raporlari_yonet'),
    path('yer-ata/<int:user_id>/', views.yer_ata, name='yer_ata'),
    path('arama/', views.all_tickets_view, name='arama'),
    path('yardim/', views.yardim_view, name='yardim'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    path('home/', views.home, name='home'),
    path('ticket_create/', views.ticket_create, name='ticket_create'),
    path('tickets/tickets/<slug:yer_slug>/', views.filtered_tickets, name='filtered_tickets'),
    path('tickets/detail/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('yer_yonetimi/', views.yer_yonetimi, name='yer_yonetimi'),
    path('yer_ekle/', views.yer_ekle, name='yer_ekle'),
    path('yer_duzenle/<int:pk>/', views.yer_duzenle, name='yer_duzenle'),
    path('secenekler/', views.secenekler, name='secenekler'),
    path('kullanici_profilini_duzenle/', views.kullanici_profilini_duzenle, name='kullanici_profilini_duzenle'),
    path('kullanici_ekle/', views.kullanici_ekle, name='kullanici_ekle'),
    path('kullanici_duzenle/<int:id>/', views.kullanici_duzenle, name='kullanici_duzenle'),
    path('kullanici_sil/<int:id>/', views.kullanici_sil, name='kullanici_sil'),
    path('ayarlari_yonet/', views.ayarlari_yonet, name='ayarlari_yonet'),
    path('dizinleri_yeniden_olustur/', views.dizinleri_yeniden_olustur, name='dizinleri_yeniden_olustur'),
    path('sifre_degistir/', views.sifre_degistir, name='sifre_degistir'),
    path('profile/', views.edit_profile, name='profile'),
    path('created-tickets/<int:location_id>/', views.created_tickets_by_location, name='created_tickets_by_location'),
    path('assigned-tickets/<int:location_id>/', views.assigned_tickets_by_location, name='assigned_tickets_by_location'),
    path('export-excel/<int:yer_id>/', export_to_excel, name='export_to_excel'),  # Yer filtreleme için olan yol
    path('export-filtered-tickets/', export_to_excel1, name='export_to_excel1'),
    path('yerler/<int:yer_id>/kullanicilar/', views.yer_kullanicilar, name='yer_kullanicilar'),
    path('yerler/<int:yer_id>/kullanici-ata/', views.kullanici_ata, name='kullanici_ata'),
    path('yerler/<int:yer_id>/kullanici-kaldir/<int:kullanici_id>/', views.kullanici_kaldir, name='kullanici_kaldir'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/tickets/<slug:yer_slug>/', views.filtered_tickets, name='filtered_tickets'),
]
