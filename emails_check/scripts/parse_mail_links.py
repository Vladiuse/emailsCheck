from emails.models import Email, Mail

mails = Mail.objects.all()
for mail in mails:
    mail.parse_links()
    mail.detect_author()