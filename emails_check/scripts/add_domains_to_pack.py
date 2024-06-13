from domains.models import Domain, DomainPack

domains_to_add = list()
with open('domains_pack.txt') as file:
    for line in file:
        domain = line.strip()
        print(domain)
        domains_to_add.append(domain)

qs = Domain.objects.filter(pk__in=domains_to_add)
print(qs.count, 'domain')
if qs.count() != len(domains_to_add):
    print('Колво доменов в бд и файле не сопадвет')
    exit()

domains_with_pack = qs.filter(pack__isnull=False)
print(domains_with_pack.count())
if domains_with_pack.exists():
    for domain in domains_with_pack:
        print(domain)
    print('Некоторые домены уже есть в паке')

domain_pack = DomainPack.objects.create(date='2024-07-12')
qs.update(pack=domain_pack)
print(domain_pack.date, domain_pack)