from django import template

register = template.Library()

@register.inclusion_tag('emails/mails_table.html')
def mails_table(mails):
    content = {
        'mails': mails,
    }
    return content


@register.inclusion_tag('emails/emails_table.html')
def emails_table(emails):
    content = {
        'emails': emails,
    }
    return content