from django.shortcuts import render, redirect
from .models import Email, Mail, MailLink, EmailPack
from django.db.models import Count, Prefetch
from django.http import HttpResponse
from datetime import datetime


def email_pack_list(request):
    email_pack_list = EmailPack.objects.all()
    content = {
        'email_pack_list': email_pack_list,
    }
    return render(request, 'emails/email_pack_list.html', content)


def email_pack(request, email_pack_id):
    email_pack = EmailPack.objects.get(pk=email_pack_id)
    emails = Email.objects.filter(email_pack=email_pack).prefetch_related('mails').annotate(
        mails_count=Count('mail'))
    total_mails = sum(email.mails_count for email in emails)
    content = {
        'email_pack': email_pack,
        'emails': emails,
        'total_mails': total_mails,
        'desc': email_pack.desc,
    }
    return render(request, 'emails/emails_list.html', content)


def emails_send_by(request):
    if request.method == 'POST':
        print(request.POST)
        date = request.POST['date']
        return redirect('emails:emails_send_by_date', date=date)
    else:
        return render(request, 'emails/emails_send_by.html')

def emails_send_by_date(request, date):
    """
    Список пролитых в указаную дату
    """
    date = datetime.strptime(date, '%Y-%m-%d').date()
    emails = Email.objects.select_related('email_pack').prefetch_related(
        'mails'
    ).filter(mail__send_time__date=date).annotate(mails_count=Count('mail')).order_by('-email_pack__date')
    total_mails = sum(email.mails_count for email in emails)
    content = {
        'emails': emails,
        'total_mails': total_mails,
        'date': date,
    }
    return render(request, 'emails/date_send.html', content)


def emails(request):
    emails = Email.objects.prefetch_related('mails').annotate(mails_count=Count('mail'))
    content = {
        'emails': emails,
    }
    return render(request, 'emails/emails_list.html', content)


def email(request, email_login):
    email = Email.objects.get(pk=email_login)
    mails = Mail.objects.filter(email=email)
    content = {
        'email': email,
        'mails': mails,
    }
    return render(request, 'emails/email.html', content)


def mail(request, mail_id):
    mail = Mail.objects.get(pk=mail_id)
    content = {
        'mail': mail,
        'email': mail.email,
    }
    return render(request, 'emails/mail.html', content)


def alien_links(request):
    alien_links = MailLink.objects.filter(domain__isnull=True).select_related('mail').order_by('-mail__send_time')
    content = {
        'alien_links': alien_links,
    }
    return render(request, 'emails/alien_links.html', content)


def test(request):
    date = datetime.today().date()
    teams_stat = MailLink.objects.select_related('team'). \
        filter(mail__send_time__date=date).values('team').annotate(mail_links_count=Count('team')).order_by('-mail_links_count')
    author_mails_stat = Mail.objects.filter(send_time__date='2024-06-17').values('author_email').annotate(
        count=Count('author_email')).order_by('-count')
    mails = Mail.objects.select_related('email__email_pack').filter(send_time__date=date)
    packs = dict()
    for mail in mails:
        try:
            packs[mail.email.email_pack] += 1
        except KeyError:
            packs[mail.email.email_pack] = 1
    packs = [(pack, mails_count) for pack, mails_count in packs.items()]
    packs.sort(key=lambda item: item[0].date, reverse=True)
    content = {
        'mails': mails,
        'date': date,
        'packs': packs,
        'teams_stat': teams_stat,
        'author_mails_stat': author_mails_stat,
    }
    return render(request, 'emails/test.html', content)
