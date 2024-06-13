from emails.models import Email, Mail
from datetime import datetime
from django.db.models import Count
from bs4 import BeautifulSoup
from time import sleep
import time

new_emails = Email.objects.filter(last_update__isnull=True)
print(new_emails.count())
res = input('Continue?')
if res != 'y':
    exit()
start = datetime.now()
for email in new_emails:
    email.update_mails()

end = datetime.now()
print('time:' ,end - start)