from django.contrib import admin
from .models import EmailPack
from django.db.models import Count

class EmailPackAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'date', 'emails_count']
    list_display_links = ['pk', 'name']
    @admin.display(description="EMails in pack")
    def emails_count(self,obj):
        mails_count = obj.emails.count()
        return str(mails_count)

admin.site.register(EmailPack, EmailPackAdmin)
