from django import template
register = template.Library()

@register.filter
def minutes(seconds):
    if seconds == 0: #Perm
        seconds = 'PERM'
    elif seconds < 3600: #Minuty
        minutes = seconds / 60
        seconds = ("%d minut" % (minutes))
    elif seconds <= 86400: #Godziny
        minutes = seconds / 60
        hours = minutes / 60
        seconds = ("%d godzina(y)" % (hours))
    elif seconds <= 604800: #Dni
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        seconds = ("%d dni" % (days))
    elif seconds <= 7889231: #Tygodnie
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        week = days / 7
        seconds = ("%d tygodnie" % (week))
    else: #Miesiące
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        week = days / 7
        month = week / 3
        seconds = ("%d miesiecy" % (month))
        
    return seconds
    