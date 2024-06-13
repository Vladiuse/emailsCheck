from django.contrib import admin
from .models import Domain, DomainPack

class DomainPackAdmin(admin.ModelAdmin):
    list_display = ['pk', 'date', 'domains_count']
    list_display_links = ['pk', 'date', ]

    @admin.display(description='Domains Count')
    def domains_count(self, obj):
        return str(obj.domains.count())


admin.site.register(DomainPack, DomainPackAdmin)

