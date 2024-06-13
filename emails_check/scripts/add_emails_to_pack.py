from emails.models import Email, EmailPack

emails_to_pack = list()
with open('email_pack.txt') as file:
    for line in file:
        email = line.strip()
        emails_to_pack.append(email)

print('Emails to add:', len(emails_to_pack))
qs = Email.objects.filter(pk__in=emails_to_pack)
not_have_pack_qs = qs.filter(email_pack__isnull=False)
if not_have_pack_qs.exists():
    for email in not_have_pack_qs:
        print(email)
    print('Not all emails dont have pack!')
    exit()

# mail_pack = EmailPack.objects.create(
#     name='24.04',
# )
mail_pack = EmailPack.objects.get(
    name='24.04',
)
qs.update(email_pack=mail_pack)
print(mail_pack)