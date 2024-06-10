from emails.models import Email

with open('emails_to_create.txt') as file:
    for line in file:
        line = line.strip()
        login, password = line.split('\t')
        print(login, password)
        Email.objects.create(
            login=login,
            password=password,
        )