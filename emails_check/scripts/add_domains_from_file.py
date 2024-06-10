from domains.models import Domain
from django.db import IntegrityError

created_count = 0
with open('domains_to_create.txt') as file:
    for line in file:
        domain = line.strip()
        if domain:
            try:
                Domain.objects.create(
                    name=domain
                )
                created_count += 1
            except Domain.DoesNotExist:
                print(f'{domain} already id bd')
            except IntegrityError as error:
                print(domain, error)

print('Created new:', created_count)
print('Total', Domain.objects.count())

