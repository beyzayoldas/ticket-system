import csv
from datetime import timezone
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import AdminUserChangeForm, TicketUpdateForm,  UserProfileForm, TicketForm, LoginForm, YerForm
from .models import Ticket, TicketUpdate,  Yer
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket
from django.shortcuts import render, redirect
from .forms import TicketForm
from django.conf import settings
from .forms import TicketForm
from .models import CustomUser
from django.template.loader import render_to_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Yer, CustomUser  
from django.shortcuts import render, get_object_or_404
from .models import Yer, Ticket
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from PIL import Image
import base64
from io import BytesIO

from io import BytesIO
import base64
from PIL import Image

import tempfile
from PIL import Image
import base64
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from weasyprint import HTML

import os
import base64

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Yer, Ticket
from django.template.loader import render_to_string

from weasyprint import HTML

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string

from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
from django.http import HttpResponse

def download_pdf(request, location_id):
    yer = get_object_or_404(Yer, id=location_id)
    open_tickets = Ticket.objects.filter(company=yer, status='open')
    closed_tickets = Ticket.objects.filter(company=yer, status='closed')

    # Grafik oluşturma ve base64 dönüştürme
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Açık Talepler', 'Kapalı Talepler'], [open_tickets.count(), closed_tickets.count()], color=['blue', 'orange'])
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'yer': yer,
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'open_tickets_count': open_tickets.count(),
        'closed_tickets_count': closed_tickets.count(),
        'chart_image': f'data:image/png;base64,{image_base64}',
    }

    html_string = render_to_string('tickets/filtered_rapor.html', context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{yer.goruntu_adi}_rapor.pdf"'
    return response





from django.shortcuts import render

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from io import BytesIO
import base64

import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64




from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.conf import settings




@login_required
def download_arama_pdf(request):
    query = request.GET.get('q', '')
    tickets = Ticket.objects.all()

    if query:
        tickets = tickets.filter(
            Q(summary__icontains=query) |
            Q(details__icontains=query) |
            Q(company__goruntu_adi__icontains=query)
        )

    context = {
        'tickets': tickets
    }

    # Şablondan HTML oluşturma
    html_string = render_to_string('tickets/arama.html', context, request=request)

    # CSS dosyasını yükleme
    css_path = settings.BASE_DIR / "static" / "css" / "pdf_style.css"

    # PDF oluşturma
    pdf_file = HTML(string=html_string).write_pdf(stylesheets=[str(css_path)])

    # PDF'i HTTP yanıtı olarak döndürme
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="arama_raporu.pdf"'
    return response



def filtered_rapor(request, location_id):
    yer = get_object_or_404(Yer, id=location_id)
    open_tickets = Ticket.objects.filter(company=yer, status='open')
    closed_tickets = Ticket.objects.filter(company=yer, status='closed')

    # Grafik oluşturma
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x=['Açık Talepler', 'Kapalı Talepler'],
        y=[open_tickets.count(), closed_tickets.count()],
        palette='coolwarm',  # Daha modern bir renk paleti
        ax=ax
    )

    # Başlık ve eksen etiketleri
    ax.set_title('Taleplerin Analizi', fontsize=16, fontweight='bold')
    ax.set_ylabel('Taleplerin Sayısı', fontsize=14)
    ax.set_xlabel('Talep Durumları', fontsize=14)

    # Her çubuğun üzerine değer yazdırma
    for p in ax.patches:
        ax.annotate(
            f'{int(p.get_height())}', 
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontsize=12, fontweight='bold'
        )

    # Grafiği base64 formatına dönüştürme
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'yer': yer,
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'open_tickets_count': open_tickets.count(),
        'closed_tickets_count': closed_tickets.count(),
        'chart_image': f'data:image/png;base64,{image_base64}',
    }

    return render(request, 'tickets/filtered_rapor.html', context)




def raporlari_yonet(request):
    yer_list = Yer.objects.all()  
    report_data = []

    for yer in yer_list:
        open_tickets = Ticket.objects.filter(company=yer, status='open').count()  
        closed_tickets = Ticket.objects.filter(company=yer, status='closed').count()

        report_data.append({
            'yer': yer,
            'open_tickets': open_tickets,
            'closed_tickets': closed_tickets
        })

    return render(request, 'tickets/raporlari_yonet.html', {'report_data': report_data})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Yer

def yer_sil_yonetim(request, yer_id):
    yer = get_object_or_404(Yer, id=yer_id)
    yer.delete()
    messages.success(request, f"{yer.goruntu_adi} başarıyla silindi.")
    return redirect('yer_yonetimi')

def yer_sil_ata(request, user_id, yer_id):
    user = get_object_or_404(CustomUser, id=user_id)
    yer = get_object_or_404(Yer, id=yer_id)
    user.yerler.remove(yer)
    messages.success(request, f"{yer.goruntu_adi} kullanıcıdan başarıyla kaldırıldı.")
    return redirect('yer_ata', user_id=user_id)



def yer_ata(request, user_id):
    user = CustomUser.objects.get(id=user_id)  # Kullanıcıyı alıyoruz
    yerler = Yer.objects.all()  # Tüm yerler listeleniyor
    mevcut_yerler = user.yerler.all()  # Kullanıcının mevcut atanan yerleri
    
    if request.method == 'POST':
        yer_id = request.POST.get('yer')  # POST isteğinde gelen yer ID'sini alıyoruz
        yer = Yer.objects.get(id=yer_id)
        user.yerler.add(yer)  # Yeni yer ataması yapıyoruz
        mevcut_yerler = user.yerler.all()  # Atamadan sonra mevcut yerler güncelleniyor
        return render(request, 'tickets/yer_ata.html', {'user': user, 'yerler': yerler, 'mevcut_yerler': mevcut_yerler})

    return render(request, 'tickets/yer_ata.html', {'user': user, 'yerler': yerler, 'mevcut_yerler': mevcut_yerler})



# burada veritabanındaki tüm ticketları değil de role ve yere göre atanmış ticketları koymak istiyoruz.
from django.db.models import Case, When

 
@login_required
def all_tickets_view(request):
    user = request.user
    assigned_locations = user.yerler.all()
    query = request.GET.get('q')  # Arama sorgusu
    sort_priority = request.GET.get('sort_priority', None)  # Öncelik sıralama yönü
    sort_importance = request.GET.get('sort_importance', None)  # Önem sıralama yönü
    sort_created = request.GET.get('sort_created', None)  # Oluşturulma Tarihi sıralama yönü
 
    # Varsayılan sıralama: ID'ye göre büyükten küçüğe
    tickets = Ticket.objects.filter(company__in=assigned_locations).order_by('-id')
 
    if query:
        tickets = tickets.filter(
            Q(summary__icontains=query) |
            Q(details__icontains=query) |
            Q(company__goruntu_adi__icontains=query)
        )
 
    # Öncelik sıralaması
    if sort_priority == 'asc':
        tickets = tickets.order_by(
            Case(
                When(priority='Low', then=1),
                When(priority='Medium', then=2),
                When(priority='High', then=3),
                default=4,
            )
        )
    elif sort_priority == 'desc':
        tickets = tickets.order_by(
            Case(
                When(priority='High', then=1),
                When(priority='Medium', then=2),
                When(priority='Low', then=3),
                default=4,
            )
        )
 
    # Önem sıralaması
    if sort_importance == 'asc':
        tickets = tickets.order_by(
            Case(
                When(severity='Minor', then=1),
                When(severity='Major', then=2),
                When(severity='Critical', then=3),
                default=4,
            )
        )
    elif sort_importance == 'desc':
        tickets = tickets.order_by(
            Case(
                When(severity='Critical', then=1),
                When(severity='Major', then=2),
                When(severity='Minor', then=3),
                default=4,
            )
        )
 
    # Oluşturulma Tarihi sıralaması
    if sort_created == 'asc':
        tickets = tickets.order_by('created_at')  # Tarihe göre küçükten büyüğe
    elif sort_created == 'desc':
        tickets = tickets.order_by('-created_at')  # Tarihe göre büyükten küçüğe
 
    return render(request, 'tickets/arama.html', {'tickets': tickets})





from django.contrib.auth import get_user_model

@login_required
def kullanici_durum_degistir(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    user.is_active = not user.is_active  # Aktiflik durumunu tersine çevir
    user.save()
    return redirect('kullanicilari_yonet')  # Doğru URL adına yönlendirme




def arama_view(request):
    return render(request, 'tickets/arama.html')


def yardim_view(request):
    return render(request, 'tickets/yardim.html')  # Yardım sayfası oluşturulur


import csv
from django.http import HttpResponse
from .models import Ticket

def export_to_excel1(request):
    # HTTP cevabı CSV dosyası olarak ayarlıyoruz
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_tickets.csv"'

    # CSV yazıcısını oluşturuyoruz
    writer = csv.writer(response)
    # Sütun başlıklarını ekleyelim
    writer.writerow(['ID', 'Summary', 'Details', 'Company', 'Priority', 'Severity', 'Assigned To', 'Status', 'Created At'])

    # Arama kriterini alıyoruz
    query = request.GET.get('q', '')

    # Tüm ticket'ları filtreliyoruz (eğer arama kriteri varsa)
    if query:
        tickets = Ticket.objects.filter(summary__icontains=query)
    else:
        tickets = Ticket.objects.all()

    # Her ticket'ı CSV'ye yazıyoruz
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.summary,
            ticket.details,
            ticket.company.goruntu_adi if ticket.company else 'N/A',  # Eğer şirket boşsa 'N/A'
            ticket.priority,
            ticket.severity,
            ticket.assigned_to.username if ticket.assigned_to else 'N/A',  # Eğer atanan kişi boşsa 'N/A'
            ticket.updates.last().status if ticket.updates.last() else 'Durum Yok',  # Durum son güncellemeye bağlı
            ticket.created_at.strftime("%Y-%m-%d %H:%M")  # Oluşturulma tarihi
        ])

    return response


def export_to_excel(request, yer_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="tickets_{yer_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Summary', 'Details', 'Company', 'Priority', 'Severity'])

    tickets = Ticket.objects.filter(company__id=yer_id)

    for ticket in tickets:
        writer.writerow([
            ticket.id, 
            ticket.summary, 
            ticket.details, 
            ticket.company.goruntu_adi,  
            ticket.priority, 
            ticket.severity
        ])

    return response


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message').lower()

        # Kullanıcı mesajında belirli kelimeleri kontrol et
        if 'hello' in user_message:
            bot_message = "Merhaba! Size nasıl yardımcı olabilirim?"
        elif 'destek' in user_message and 'adım adım' in user_message:
            bot_message = (
                "Destek oluşturmak için adım adım yapmanız gerekenler şunlardır:\n"
                "1. Ana sayfadaki 'Destek Oluştur' butonuna tıklayın.\n"
                "2. Açılan formda yer alan 'Özet' ve 'Detaylar' alanlarını doldurun.\n"
                "3. İlgili kategoriyi ve öncelik seviyesini seçin.\n"
                "4. Gerekirse dosya ekleyin ve ardından 'Gönder' butonuna basın.\n"
                "5. Destek talebiniz oluşturulduktan sonra, durumu takip etmek için 'Bana Atanan' sekmesinden kontrol edebilirsiniz."
            )
        elif 'destek' in user_message:
            bot_message = "Destek oluşturmak için soldaki 'Destek Oluştur' butonunu kullanabilirsiniz."
        elif 'teşekkürler' in user_message or 'sağol' in user_message:
            bot_message = "Rica ederim! Yardımcı olabileceğim başka bir şey var mı?"
        elif 'şifre' in user_message:
            bot_message = "Şifrenizi değiştirmek için 'Profil' sayfasından 'Şifre Değiştir' seçeneğini kullanabilirsiniz."
        elif 'ticket' in user_message:
            bot_message = "Ticket durumunuzu öğrenmek için 'Bana Atanan' bölümünden kontrol edebilirsiniz."
        elif 'email' in user_message:
            bot_message = "E-posta bildirimleri için 'Ayarlar' sayfasını ziyaret edebilirsiniz."
        elif 'iletişim' in user_message or 'bize ulaşın' in user_message:
            bot_message = (
                "Bize ulaşmak için aşağıdaki yöntemleri kullanabilirsiniz:\n"
                "- Telefon: +90 545 506 5495\n"
                "- E-posta: albedestek@sirket.com\n"
                "- Adres: Soktas Caddesi No:123, Aydın, Türkiye"
            )
        elif 'çalışma saatleri' in user_message:
            bot_message = "Çalışma saatlerimiz hafta içi her gün 09:00-18:00 arasındadır. Hafta sonları kapalıyız."
        elif 'randevu' in user_message:
            bot_message = "Randevu almak için 'Bize Ulaşın' sekmesinden form doldurabilirsiniz."
        else:
            bot_message = "Üzgünüm, sorunuza uygun bir yanıt bulamadım. Lütfen tekrar deneyin."

        return JsonResponse({'message': bot_message})
    
    return JsonResponse({'message': 'Geçersiz istek.'}, status=400)



from django.db.models import Case, When

@login_required
def created_tickets_by_location(request, location_id):
    yer = get_object_or_404(Yer, id=location_id)
    tickets = Ticket.objects.filter(company=yer)

    # Sıralama Parametrelerini Al
    sort_priority = request.GET.get('sort_priority')
    sort_importance = request.GET.get('sort_importance')
    sort_created = request.GET.get('sort_created')

    # Öncelik Sıralaması
    if sort_priority == 'asc':
        tickets = tickets.order_by(
            Case(
                When(priority='Low', then=1),
                When(priority='Medium', then=2),
                When(priority='High', then=3),
                default=4,
            )
        )
    elif sort_priority == 'desc':
        tickets = tickets.order_by(
            Case(
                When(priority='High', then=1),
                When(priority='Medium', then=2),
                When(priority='Low', then=3),
                default=4,
            )
        )

    # Önem Sıralaması
    if sort_importance == 'asc':
        tickets = tickets.order_by(
            Case(
                When(severity='Minor', then=1),
                When(severity='Major', then=2),
                When(severity='Critical', then=3),
                default=4,
            )
        )
    elif sort_importance == 'desc':
        tickets = tickets.order_by(
            Case(
                When(severity='Critical', then=1),
                When(severity='Major', then=2),
                When(severity='Minor', then=3),
                default=4,
            )
        )

    # Oluşturma Tarihi Sıralaması
    if sort_created == 'asc':
        tickets = tickets.order_by('created_at')
    elif sort_created == 'desc':
        tickets = tickets.order_by('-created_at')

    return render(request, 'tickets/created_tickets_by_location.html', {'tickets': tickets, 'yer': yer})


@login_required
def assigned_tickets_by_location(request, location_id):
    yer = get_object_or_404(Yer, id=location_id)
    tickets = Ticket.objects.filter(company=yer, assigned_to=request.user)

    # Sıralama Parametrelerini Al
    sort_priority = request.GET.get('sort_priority')
    sort_importance = request.GET.get('sort_importance')
    sort_created = request.GET.get('sort_created')

    # Aynı sıralama mantığını uygula
    if sort_priority == 'asc':
        tickets = tickets.order_by(
            Case(
                When(priority='Low', then=1),
                When(priority='Medium', then=2),
                When(priority='High', then=3),
                default=4,
            )
        )
    elif sort_priority == 'desc':
        tickets = tickets.order_by(
            Case(
                When(priority='High', then=1),
                When(priority='Medium', then=2),
                When(priority='Low', then=3),
                default=4,
            )
        )

    if sort_importance == 'asc':
        tickets = tickets.order_by(
            Case(
                When(severity='Minor', then=1),
                When(severity='Major', then=2),
                When(severity='Critical', then=3),
                default=4,
            )
        )
    elif sort_importance == 'desc':
        tickets = tickets.order_by(
            Case(
                When(severity='Critical', then=1),
                When(severity='Major', then=2),
                When(severity='Minor', then=3),
                default=4,
            )
        )

    if sort_created == 'asc':
        tickets = tickets.order_by('created_at')
    elif sort_created == 'desc':
        tickets = tickets.order_by('-created_at')

    return render(request, 'tickets/assigned_tickets_by_location.html', {'tickets': tickets, 'yer': yer})


from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import Ticket, TicketUpdate  # TicketUpdate modelini ekledik

CustomUser = get_user_model()

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    users = CustomUser.objects.all()
    updates = TicketUpdate.objects.filter(ticket=ticket).order_by('-created_at')  # Ticket güncellemelerini alıyoruz

    if request.method == 'POST':
        # Yeni bir TicketUpdate oluşturuyoruz
        update = TicketUpdate(
            ticket=ticket,
            user=request.user,
            comment=request.POST.get('comment'),
            status=request.POST.get('status')
        )
        update.save()
        
        # Ticket'ı güncelliyoruz
        ticket.status = request.POST.get('status')
        ticket.assigned_to_id = request.POST.get('assigned_to')
        ticket.save()
        return redirect('ticket_detail', ticket_id=ticket.id)

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'users': users,
        'updates': updates,  # Güncellemeleri template'e gönderiyoruz
    })

from django.db.models import Count, Q

from django.db.models import Count, Q

@login_required
def kullanici_raporlar(request):
    # Ticket'ların atandığı kişilere göre rapor oluştur
    users = CustomUser.objects.annotate(
        open_tickets=Count('tickets_assigned', filter=Q(tickets_assigned__status='open')),
        closed_tickets=Count('tickets_assigned', filter=Q(tickets_assigned__status='closed'))
    )

    # Başarı oranını hesaplama
    for user in users:
        total_tickets = user.open_tickets + user.closed_tickets
        user.success_rate = (user.closed_tickets / total_tickets) * 100 if total_tickets > 0 else 0

    return render(request, 'tickets/kullanici_raporlar.html', {'users': users})


from django.shortcuts import get_object_or_404

from django.db.models import Q




from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)  # Sadece admin kullanıcıların erişimi
def kullanici_detay(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    tickets = Ticket.objects.filter(assigned_to=user).select_related('company')

    # Kapalı ve açık talepleri hesapla
    closed_tickets_count = tickets.filter(status='closed').count()
    total_tickets_count = tickets.count()
    success_rate = (closed_tickets_count / total_tickets_count * 100) if total_tickets_count > 0 else 0

    context = {
        'user': user,
        'tickets': tickets,
        'closed_tickets_count': closed_tickets_count,
        'total_tickets_count': total_tickets_count,
        'success_rate': round(success_rate, 2),
    }
    return render(request, 'tickets/kullanici_detay.html', context)




from django.db.models import Case, When
 
@login_required
def filtered_tickets(request, yer_slug):
    yer = get_object_or_404(Yer, goruntu_adi=yer_slug)
    sort_priority = request.GET.get('sort_priority', None)
    sort_importance = request.GET.get('sort_importance', None)
    sort_created = request.GET.get('sort_created', None)
 
    tickets = Ticket.objects.filter(company=yer).select_related('assigned_to', 'created_by')
 
    # Öncelik sıralaması
    if sort_priority == 'asc':
        tickets = tickets.order_by(
            Case(
                When(priority='Low', then=1),
                When(priority='Medium', then=2),
                When(priority='High', then=3),
                default=4,
            )
        )
    elif sort_priority == 'desc':
        tickets = tickets.order_by(
            Case(
                When(priority='High', then=1),
                When(priority='Medium', then=2),
                When(priority='Low', then=3),
                default=4,
            )
        )
 
    # Önem sıralaması
    if sort_importance == 'asc':
        tickets = tickets.order_by(
            Case(
                When(severity='Minor', then=1),
                When(severity='Major', then=2),
                When(severity='Critical', then=3),
                default=4,
            )
        )
    elif sort_importance == 'desc':
        tickets = tickets.order_by(
            Case(
                When(severity='Critical', then=1),
                When(severity='Major', then=2),
                When(severity='Minor', then=3),
                default=4,
            )
        )
 
    # Oluşturulma Tarihi sıralaması
    if sort_created == 'asc':
        tickets = tickets.order_by('created_at')
    elif sort_created == 'desc':
        tickets = tickets.order_by('-created_at')
 
    return render(request, 'tickets/filtered_tickets.html', {
        'tickets': tickets,
        'yer': yer
    })



# def home_view(request):
#     yerler = Yer.objects.all()
#     return render(request, 'tickets/home.html', {'yerler': yerler})



from email.mime.base import MIMEBase
from email import encoders

@login_required
def ticket_create(request):
    # Yeni ekleme: location_id sorgu parametresini al
    location_id = request.GET.get('location_id')
    initial_data = {}

    # Eğer location_id varsa, başlangıç verisine yerleştir
    if location_id:
        initial_data['company'] = location_id  # Yer bilgisini formda önceden doldur

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            form.save_m2m()

            selected_users = form.cleaned_data['email_notification']
            to_emails = [user.email for user in selected_users]

            smtp_host = "mail.soktas.com"
            smtp_port = 587
            smtp_user = "ozan.kuyumcu@soktas.com"
            smtp_password = "1WnstonBlue9@"

            from_email = smtp_user
            subject = "Yeni Ticket Oluşturuldu"

            # URL'yi oluşturma
            ticket_url = reverse('ticket_detail', args=[ticket.id])
            domain = request.get_host()
            full_url = f'http://{domain}{ticket_url}'

            # HTML içerik oluşturuluyor
            html_content = render_to_string('tickets/ticket_email_template.html', {'ticket': ticket, 'ticket_url': full_url})

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject
            msg.attach(MIMEText(html_content, 'html'))  # HTML içeriği eklendi

            if request.FILES.get('attachment'):
                attachment = request.FILES['attachment']
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{attachment.name}"')
                msg.attach(part)

            try:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

                server = smtplib.SMTP(smtp_host, smtp_port)
                server.starttls(context=context)
                server.login(smtp_user, smtp_password)

                server.sendmail(from_email, to_emails, msg.as_string())
                print("E-posta başarıyla gönderildi!")

            except Exception as e:
                print(f"E-posta gönderme hatası: {e}")

            finally:
                if server:
                    try:
                        server.quit()
                    except Exception as e:
                        print(f"Sunucudan çıkış yapılırken hata: {e}")

            return redirect('home')
    else:
        form = TicketForm(initial=initial_data)  # Yeni ekleme: başlangıç verisi ile form oluştur

    return render(request, 'tickets/ticket_create.html', {'form': form})



from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserUpdateForm  # CustomUserUpdateForm'u ekle

@login_required
def kullanici_duzenle(request, id):
    user = get_object_or_404(get_user_model(), id=id)  # Düzenlenecek kullanıcıyı bulun
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)  # CustomUserUpdateForm'u kullanarak güncelle
        if form.is_valid():
            form.save()  # Form geçerliyse kaydedin
            messages.success(request, 'Kullanıcı bilgileri başarıyla güncellendi.')
            return redirect('kullanicilari_yonet')  # Güncellemeden sonra yönlendirme
    else:
        form = CustomUserUpdateForm(instance=user)  # GET isteği için formu mevcut kullanıcıyla doldurun
    return render(request, 'tickets/kullanici_duzenle.html', {'form': form, 'user': user})


@login_required
def kullanici_sil(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Kullanıcı başarıyla silindi.')
        return redirect('kullanicilari_yonet')
    return render(request, 'tickets/kullanici_sil_onay.html', {'user': user})



def logout_view(request):
    logout(request)
    return redirect('login')  # Logout işleminden sonra kullanıcıyı login sayfasına yönlendirin.


@login_required
def home(request):
    user = request.user

    # Kullanıcıya atanmış yerler
    assigned_locations = user.yerler.all()

    # Genel yerler (tüm kullanıcılara açık olanlar)
    general_locations = Yer.objects.filter(genel_yap=True)

    yer_ticket_count = []

    # Kullanıcıya atanmış yerler ve genel yerler üzerinde döngü
    for yer in assigned_locations.union(general_locations):
        # Kullanıcıya atanmış olan ticket sayısını hesapla
        assigned_ticket_count = Ticket.objects.filter(company=yer, assigned_to=request.user).count()

        # Kullanıcının yarattığı ticket sayısını hesapla
        created_ticket_count = Ticket.objects.filter(company=yer, created_by=request.user).count()

        yer_ticket_count.append({
            'yer': yer,
            'assigned_ticket_count': assigned_ticket_count,
            'created_ticket_count': created_ticket_count
        })

    context = {
        'yer_ticket_count': yer_ticket_count
    }
    return render(request, 'tickets/home.html', context)




from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Hatalı kullanıcı adı veya parola.')  # Mesaj oluşturuldu
    else:
        form = LoginForm()
    return render(request, 'tickets/login.html', {'form': form})





@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})


@login_required
@user_passes_test(lambda u: u.is_staff)
def kullanici_profilini_duzenle(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Oturumu güncelle
            messages.success(request, 'Profil başarıyla güncellendi.')
            return redirect('home')  # Kullanıcıyı ana sayfaya yönlendir
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'tickets/kullanici_profilini_duzenle.html', {'form': form})

@login_required
def yer_ekle(request):
    if request.method == 'POST':
        form = YerForm(request.POST)
        if form.is_valid():
            yer = form.save(commit=False)  # Yer nesnesini kaydetmeden al
            yer.save()  # ID oluşturulması için önce kaydet
            if yer.genel_yap:
                # Tüm kullanıcıları bu yere ekle
                all_users = CustomUser.objects.all()
                yer.kullanicilar.set(all_users)
            messages.success(request, 'Yer başarıyla eklendi.')
            return redirect('yer_yonetimi')
    else:
        form = YerForm()
    return render(request, 'tickets/yer_ekle.html', {'form': form})




@login_required
def yer_duzenle(request, pk):
    yer = get_object_or_404(Yer, pk=pk)
    if request.method == 'POST':
        form = YerForm(request.POST, instance=yer)
        if form.is_valid():
            yer = form.save(commit=False)
            if yer.genel_yap:
                # Tüm kullanıcıları bu yere ekle
                all_users = CustomUser.objects.all()
                yer.kullanicilar.set(all_users)
            else:
                yer.kullanicilar.clear()  # Tüm kullanıcıları kaldır
            yer.save()
            messages.success(request, 'Yer başarıyla güncellendi.')
            return redirect('yer_yonetimi')
    else:
        form = YerForm(instance=yer)
    return render(request, 'tickets/yer_duzenle.html', {'form': form, 'yer': yer})


@login_required
def yer_yonetimi(request):
    # Tüm yerleri listele
    yerler = Yer.objects.all()

    return render(request, 'tickets/yer_yonetimi.html', {'yerler': yerler})




from django.shortcuts import render, redirect, get_object_or_404
from .models import Yer, Kullanici


from .forms import KullaniciAtaForm
from .models import CustomUser, Yer  # Kullanıcı modelini ve Yer modelini import edelim

from django.shortcuts import render, get_object_or_404, redirect
from .models import Yer, CustomUser
from .forms import KullaniciAtaForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Yer, Kullanici, CustomUser
from django.contrib import messages


@login_required
def yer_kullanicilar(request, yer_id):
    yer = get_object_or_404(Yer, id=yer_id)
    kullanicilar = yer.kullanicilar.all()

    # Kullanıcılar için `Kullanici` modelinden rol bilgilerini çekiyoruz
    kullanici_rolleri = []
    for kullanici in kullanicilar:
        kullanici_rolu = Kullanici.objects.filter(login_name=kullanici.username).first()
        if kullanici_rolu:
            kullanici_rolleri.append({'user': kullanici, 'role': kullanici_rolu.role})
        else:
            kullanici_rolleri.append({'user': kullanici, 'role': 'Rol atanmadı'})

    available_users = CustomUser.objects.exclude(id__in=[kullanici.id for kullanici in kullanicilar])

    context = {
        'yer': yer,
        'kullanicilar': kullanici_rolleri,  # Rol ile birlikte kullanıcılara erişiyoruz
        'available_users': available_users,
    }
    return render(request, 'tickets/yer_kullanicilar.html', context)



def kullanici_kaldir(request, yer_id, kullanici_id):
    yer = get_object_or_404(Yer, id=yer_id)
    kullanici = get_object_or_404(CustomUser, id=kullanici_id)
    yer.kullanicilar.remove(kullanici)  # Kullanıcıyı yerden kaldır
    messages.success(request, f'{kullanici.username} başarıyla {yer.goruntu_adi} adlı yerden kaldırıldı.')
    return redirect('yer_kullanicilar', yer_id=yer.id)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Yer, CustomUser, Kullanici

def kullanici_ata(request, yer_id):
    yer = get_object_or_404(Yer, id=yer_id)
    
    if request.method == 'POST':
        custom_user_id = request.POST.get('kullanici')
        custom_user = get_object_or_404(CustomUser, id=custom_user_id)
        rol = request.POST.get('rol')
        
        # Kullanıcıyı oluştur veya getir
        kullanici, created = Kullanici.objects.get_or_create(
            login_name=custom_user.username,
            defaults={'role': rol, 'full_name': f'{custom_user.first_name} {custom_user.last_name}'}
        )

        if not created:
            # Eğer zaten var ise rolü güncelle
            kullanici.role = rol
            kullanici.save()

        # Yer ile kullanıcıyı ilişkilendir
        yer.kullanicilar.add(custom_user)

        return redirect('yer_kullanicilar', yer_id=yer.id)
    else:
        return redirect('yer_kullanicilar', yer_id=yer.id)




@login_required
def secenekler(request):
    return render(request, 'tickets/secenekler.html')


@login_required
def kullanicilari_yonet(request):
    query = request.GET.get('q', '')
    User = get_user_model()
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        users = User.objects.all()

    return render(request, 'tickets/kullanicilari_yonet.html', {'users': users, 'query': query})




@login_required
def ayarlari_yonet(request):
    return render(request, 'tickets/ayarlari_yonet.html')

@login_required
def dizinleri_yeniden_olustur(request):
    return render(request, 'tickets/dizinleri_yeniden_olustur.html')

@login_required
def sifre_degistir(request):
    return render(request, 'tickets/sifre_degistir.html')

@login_required
def edit_profile(request):
    return render(request, 'tickets/edit_profile.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def kullanici_ekle(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kullanıcı başarıyla oluşturuldu.')
            return redirect('kullanicilari_yonet')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tickets/kullanici_ekle.html', {'form': form})