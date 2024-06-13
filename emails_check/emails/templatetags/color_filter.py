from django import template

register = template.Library()


def date_color(date):
    if date:
        print(date, type(date))
        if date.day % 2 == 0:
            return '#7b9cdf'
        else:
            return '#DDFFF7'
    return 'not_date'

def date_d(date):
    return f'{date.day} {date}'


register.filter("date_color", date_color)
register.filter("date_d", date_d)