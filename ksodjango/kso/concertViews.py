from ConcertCalendarEvent import ConcertCalendarEvent
from models import *
from django.shortcuts import get_object_or_404
from django.http import Http404
from datetime import date
import glob
from os.path import *
from otherViews import render_to_response_with_extra_data
import settings


# noinspection PyUnusedLocal
def downloadConcert(request, concert_id, member):
    concert = get_object_or_404(Concert, pk=concert_id)
    return ConcertCalendarEvent(concert, member)()


def concertDetail(request, member, **kwargs):
    try:
        if not 'concert_id' in kwargs:
            year = int(kwargs['year'])
            month = int(kwargs['month'])
            month_start = date(year, month, 1)
            month += 1
            if month == 13:
                month = 1
                year += 1
            month_end = date(year, month, 1)
            concerts = Concert.objects.filter(dateAndTime__gte=month_start).filter(dateAndTime__lt=month_end)
            if not concerts:
                raise Http404
            concert = concerts[0]
        else:
            concert_id = kwargs['concert_id']
            if concert_id == "next":
                concerts = Concert.objects.filter(dateAndTime__gte=date.today()).order_by("dateAndTime")
                if not concerts:
                    raise Concert.DoesNotExist
                concert = concerts[0]
            else:
                concert = Concert.objects.get(id=concert_id)
    except Concert.DoesNotExist:
        raise Http404
    downloads = []

    flyers = glob.glob(settings.MEDIA_ROOT + "/flyers/KSO flyer {0.dateAndTime:%Y%m%d}*.*".format(concert))
    for flyer in flyers:
        flyerUrl = settings.MEDIA_URL + flyer[len(settings.MEDIA_ROOT) + 1:]
        if flyer.count(" 2up.pdf") > 0:
            downloads = downloads + [("Flyer (2 side-by-side on A4)", flyerUrl, getsize(flyer), "pdf")]
        elif flyer.count(".pdf") > 0:
            downloads = downloads + [("Flyer (single on A5)", flyerUrl, getsize(flyer), "pdf")]
        elif flyer.count(".jpg") > 0:
            downloads = downloads + [("Flyer (JPEG for Facebook)", flyerUrl, getsize(flyer), "jpg")]

    programmes = glob.glob(settings.MEDIA_ROOT + "/programmes/KSO programme {0.dateAndTime:%Y%m%d}.pdf".format(concert))
    if (concert.dateAndTime.date() < date.today()) and programmes:
        downloads = downloads + [("Programme", settings.MEDIA_URL + programmes[0][len(settings.MEDIA_ROOT) + 1:],
                                  getsize(programmes[0]), "pdf")]

    image = concert.image()

    soundClips = []
    for concertPiece in concert.piecesInOrder():
        for soundClip in concertPiece.soundClipsInOrder():
            soundClips = soundClips + [soundClip.soundCloudEmbedCode]

    if concert.dateAndTime.date() < date.today():
        concert.ticketLink = ""

    return render_to_response_with_extra_data(request, "concertdetail.html",
                                              {'concert': concert, 'downloads': downloads, 'image': image,
                                               'soundClips': soundClips,
                                               'showIcs': concert.dateAndTime.date() >= date.today()}, member)