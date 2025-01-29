from django.contrib import admin
from .models import Yer, Ticket
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# CustomUser için admin paneli ayarları
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('language',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Yer modeli için admin paneli ayarları
class YerAdmin(admin.ModelAdmin):
    list_display = ('goruntu_adi', 'kisa_ad', 'genel_yap')

admin.site.register(Yer, YerAdmin)

# Ticket modeli için admin paneli ayarları
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['summary', 'company', 'priority', 'severity', 'assigned_to']
    search_fields = ['summary', 'details']
    list_filter = ['priority', 'severity', 'company']

# Admin paneli başlıklarını özelleştiriyoruz
admin.site.site_header = "Destek Sistemi Yönetim Paneli"  # Admin panelinin üst başlığı
admin.site.site_title = "Destek Sistemi"                 # Tarayıcı sekme başlığı
admin.site.index_title = "Hoş Geldiniz Destek Yönetimi"  # Ana sayfa başlığı