from django.shortcuts import render
from .models import Email, Mail, MailLink
from django.db.models import Count
from django.http import HttpResponse


def emails(request):
    emails = Email.objects.prefetch_related('mail_set').annotate(mails_count=Count('mail'))
    content = {
        'emails': emails,
    }
    return render(request, 'emails/emails_list.html', content)


def email(request, email_login):
    email = Email.objects.get(pk=email_login)
    content = {
        'email': email,
    }
    return render(request, 'emails/email.html', content)


def mail_html(request, mail_id):
    mail = Mail.objects.get(pk=mail_id)
    return HttpResponse(mail.html_text)


def alien_links(request):
    alien_links = MailLink.objects.filter(domain__isnull=True).select_related('mail').order_by('-mail__send_time')
    content = {
        'alien_links': alien_links,
    }
    return render(request, 'emails/alien_links.html', content)
