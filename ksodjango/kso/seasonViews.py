import calendar
from datetime import date
from django.http import Http404
from django.shortcuts import get_object_or_404
from kso.ConcertCalendarEvent import SeasonCalendarEvent
from otherViews import render_to_response_with_extra_data
from models import Season


# noinspection PyUnusedLocal
def downloadSeason(request, season_id, member):
    season = get_object_or_404(Season, pk=season_id)
    return SeasonCalendarEvent(season, member)()


def seasonDetail(request, season_id, member):
    if season_id == "next":
        futureSeasons = Season.objects.filter(endDate__gte=date.today()).order_by("startDate")
        if not futureSeasons:
            raise Http404
        #if futureSeasons.count() <= 1:
        raise Http404
        #season = futureSeasons[1]
    elif season_id == "this":
        futureSeasons = Season.objects.filter(endDate__gte=date.today()).order_by("startDate")
        if not futureSeasons:
            raise Http404
        season = futureSeasons[0]
    else:
        season = get_object_or_404(Season, pk=season_id)
    htmlCalendar = calendar.HTMLCalendar()
    htmlCalendar.setfirstweekday(calendar.SUNDAY)
    firstConcert = season.concert_set.all().order_by("dateAndTime")[0]
    start = firstConcert.dateAndTime
    if firstConcert.rehearsal_set.all():
        start = firstConcert.rehearsal_set.all().order_by("start")[0].start
    months = [htmlCalendar.formatmonth(start.year + int((start.month + i - 1) / 12), (start.month + i - 1) % 12 + 1) for
              i in range(12)]
    td_join = lambda a, b: a + '</td><td>' + b
    tr_join = lambda a, b: a + '</td></tr><tr><td>' + b
    cal = reduce(tr_join, [reduce(td_join, months[i:i + 3]) for i in range(0, 12, 3)])
    cal = '<tr><td>' + cal + '</td></tr>'
    if member == "m/":
        return render_to_response_with_extra_data(request, "seasoncalendar.html", {'calendar': cal, 'season': season},
                                                  member)
    return render_to_response_with_extra_data(request, "seasondetail.html", {'calendar': cal, 'season': season}, "")
