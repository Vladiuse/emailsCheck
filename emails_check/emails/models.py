from django.db import models
from django.core.files.base import ContentFile
import os
import imaplib, email
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from domains.models import Domain


def get_domain_from_url(url: str) -> str:
    parse = urlparse(url)
    full_domain = parse.hostname
    if full_domain:
        parts = full_domain.split('.')
        domain = '.'.join(parts[-2:])
        return domain
    else:
        return ''


def raw_date_to_date(date: str):
    date = date.replace('(GMT)', '')
    date = date.strip()
    try:
        date_tz = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
        date = date_tz.replace(tzinfo=None)
        return date
    except ValueError:
        return None


def delete_field_file(*fields):
    for field in fields:
        if field:
            if os.path.exists(field.path):
                os.remove(field.path)


class EmailPack(models.Model):
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True)

    def __str__(self):
        return f'EmailPack: {self.name}'
class Email(models.Model):
    email_pack = models.ForeignKey(
        EmailPack,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='emails',
        related_query_name='email',
    )
    login = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    emails_count = models.PositiveIntegerField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    imap_error = models.TextField(blank=True)

    def __str__(self):
        return str(self.login)

    def update_mails(self, delete_old_mails=False):
        if delete_old_mails:
            self.delete_mails()
        try:
            mail = imaplib.IMAP4_SSL("imap.firstmail.ltd", port=993)
            mail.login(str(self.login), str(self.password))
            status, messages = mail.select('INBOX')
            messages_count = int(messages[0]) + 1
            self.emails_count = messages_count
            self.last_update = datetime.now()
            print(f'On {self} find {messages_count} mails')
            for i in range(1, messages_count):
                res, raw_msg = mail.fetch(str(i), '(RFC822)')
                for response in raw_msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject = msg['subject']
                        raw_date = msg['date']
                        _from = msg['from']
                        html = b''
                        for part in msg.walk():
                            ctype = part.get_content_type()
                            if ctype == 'text/html':
                                html = part.get_payload(decode=True)
                        Mail.objects.create(
                            email=self,
                            subject=subject,
                            author=_from,
                            send_time=raw_date_to_date(raw_date),
                            raw_send_time=raw_date,
                            raw=ContentFile(str(msg), name='raw.txt'),
                            html=ContentFile(html, name='raw.html'),
                        )
            self.save()
        except imaplib.IMAP4_SSL.error as error:
            print(self, error)
            self.imap_error = str(error)
            self.save()

    def delete_mails(self):
        mails = Mail.objects.filter(email=self)
        mails.delete()



class MailQuerySet(models.QuerySet):

    def delete(self):
        for obj in self:
            obj.delete_mails_files()
        super().delete()


class Mail(models.Model):
    objects = MailQuerySet.as_manager()
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='mails', related_query_name='mail')
    subject = models.CharField(max_length=255)
    raw_send_time = models.CharField(max_length=255)
    send_time = models.DateTimeField(blank=True, null=True)
    author = models.CharField(max_length=255)
    html = models.FileField(upload_to='media/html_emails', blank=True)
    raw = models.FileField(upload_to='media/emails_raw', blank=True)

    def detect_send_time(self):
        send_time = raw_date_to_date(str(self.raw_send_time))
        if send_time:
            self.send_time = send_time
            self.save()

    def delete_mails_files(self):
        fields = (self.html, self.raw)
        delete_field_file(*fields)

    @property
    def html_text(self):
        with open(self.html.path) as file:
            return file.read()

    def parse_links(self, delete_old_links=False):
        if delete_old_links:
            self.links.all().delete()
        soup = BeautifulSoup(self.html, 'html.parser')
        links = soup.find_all('a')
        print(self, len(links))
        MailLink.create_links(self, *links)


class MailLink(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, related_name='links', related_query_name='link')
    raw_html_link = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, blank=True, null=True)

    @staticmethod
    def create_links(mail: Mail, *links):
        to_create = []
        for link in links:
            try:
                href = link['href']
            except KeyError:
                href = ''
            domain_string = get_domain_from_url(href)
            try:
                domain = Domain.objects.get(pk=domain_string)
            except Domain.DoesNotExist:
                domain = None
            mail_link = MailLink(
                mail=mail,
                raw_html_link=str(link),
                link=href,
                domain=domain
            )
            to_create.append(mail_link)
        MailLink.objects.bulk_create(to_create)
