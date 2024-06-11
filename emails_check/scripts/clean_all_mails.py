from emails.models import Email, Mail

res = input('Delete all mails?')
if res != 'y':
    print('Exit')
    exit()
Mail.objects.all().delete()

Email.objects.update(emails_count=0,last_update=None,imap_error='')