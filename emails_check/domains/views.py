from django.shortcuts import render
from .models import Domain, DomainPack
from django.db.models import Count
from emails.models import Mail, MailLink
from django.http import HttpResponse
# def domains_pack(request):
#     domains_pack = DomainPack.objects.all()
#     content = {
#         'domains_pack': domains_pack,
#     }
#     return render(request, 'domains/domains_pack.html', content)

def domains_list(request):
    domains = Domain.objects.select_related('pack').order_by('-pack__date').prefetch_related(
        'mail_links'
    ).annotate(mail_links_count=Count('mail_link'))
    content= {
        'domains': domains,
    }
    return render(request, 'domains/domains_list.html', content)


def domain(request, domain_id):
    domain = Domain.objects.get(pk=domain_id)
    domain_mails = Mail.objects.filter(link__domain=domain)
    content = {
        'domain': domain,
        'mails': domain_mails,
    }
    return render(request, 'domains/domain.html', content)

