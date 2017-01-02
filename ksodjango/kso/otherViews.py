from datetime import datetime, date
import glob
from os.path import *
from django.core.mail import send_mail
from django.core.servers.basehttp import FileWrapper
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from kso.forms import mailingListForm, DivErrorList
from models import Conductor, Venue, Rehearsal, SpecialPage, Concert, Composer, Soloist, Image, SoundClip
import settings


# noinspection PyUnusedLocal
def download(request, fileName):
    fileName = settings.MEDIA_ROOT + fileName[5:]
    ext = splitext(fileName)[1]
    mimeType = "application/pdf"
    if ext == u'.jpg' or ext == u'.jpeg':
        mimeType = "image/jpeg"
    response = HttpResponse(FileWrapper(open(fileName)))
    response['Content-Type'] = mimeType
    name = split(fileName)[1]
    response['Content-Disposition'] = 'attachment; filename={0}'.format(name)
    return response


def venueDetail(request, venue_id, member):
    venue = get_object_or_404(Venue, pk=venue_id)
    return render_to_response_with_extra_data(request, "venuedetail.html", {'venue': venue, 'image': venue.image()},
                                              member)


def conductorDetail(request, conductor_id, member):
    conductor = get_object_or_404(Conductor, pk=conductor_id)
    return render_to_response_with_extra_data(request, "conductordetail.html",
                                              {'conductor': conductor, 'image': conductor.image()}, member)


def soloistDetail(request, soloist_id, member):
    soloist = get_object_or_404(Soloist, pk=soloist_id)
    return render_to_response_with_extra_data(request, "soloistdetail.html",
                                              {'soloist': soloist, 'image': soloist.image()}, member)


def composerDetail(request, composer_id, member):
    composer = get_object_or_404(Composer, pk=composer_id)
    return render_to_response_with_extra_data(request, "composerdetail.html",
                                              {'composer': composer, 'image': composer.image()}, member)


def specialPage(request, page_name, member):
    pageObject = get_object_or_404(SpecialPage, name=page_name)
    return render_to_response_with_extra_data(request, "specialpage.html", {'page': pageObject}, member)


def whereTo(request):
    forthcoming = Rehearsal.objects.filter(start__gte=datetime.now()).order_by("start")
    if not forthcoming:
        raise Http404
    return render_to_response("whereto.html", {'rehearsal': forthcoming[0]}, context_instance=RequestContext(request))


def archive(request, member):
    concerts = Concert.objects.order_by('dateAndTime').reverse()
    return render_to_response_with_extra_data(request, "archive.html", {'concerts': concerts}, member)


def shop(request):
    return render_to_response("shop.html", context_instance=RequestContext(request))


def gallery(request, member):
    photos = Image.objects.filter(isInGallery=1)
    return render_to_response_with_extra_data(request, "gallery.html", {'photos': photos}, member)


def thanks(request):
    return render_to_response("thanks.html", context_instance=RequestContext(request))


def mailingList(request):
    if request.method == "POST":
        form = mailingListForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            send_mail('Mailing list sign up', '''The following registration for the mailing list has been received:

First name: {0}
Last name: {1}
Email addres: {2}'''.format(form.cleaned_data["firstName"], form.cleaned_data["lastName"],
                            form.cleaned_data["emailAddress"]),
                      'web.master@kso.org.uk', ['david@musgroves.us', 'jo.johnson@kso.org.uk'])
            return HttpResponseRedirect('/thanks/')
    else:
        form = mailingListForm(error_class=DivErrorList)
    return render_to_response("mailinglist.html", {'form': form}, context_instance=RequestContext(request))


def render_to_response_with_extra_data(request, view, extraData, member):
    extraData['member'] = (member == "m/")
    extraData['WORKING_OFFLINE'] = settings.WORKING_OFFLINE
    if Concert.objects.filter(dateAndTime__gte=date.today()).order_by("dateAndTime").count() > 0:
        extraData['next_concert'] = Concert.objects.filter(dateAndTime__gte=date.today()).order_by("dateAndTime")[0]
    else:
        extraData['next_concert'] = Concert.objects.order_by("-dateAndTime")[0]
    return render_to_response(view, extraData, context_instance=RequestContext(request))


def error404(request):
    return render_to_response_with_extra_data(request, "404.html", {}, False)


def home(request, member):
    content = ""
    if SpecialPage.objects.filter(name__exact='home'):
        content = SpecialPage.objects.get(name__exact='home').content
    concerts = Concert.objects.filter(dateAndTime__gte=date.today()).order_by("dateAndTime")
    if not concerts:
        raise Concert.DoesNotExist
    concert = concerts[0]
    secondConcert = concerts[1]
    image = concert.image()
    return render_to_response_with_extra_data(request, "home.html",
                                              {'content': content, 'concert': concert, 'secondConcert': secondConcert,
                                               'image': image}, member)


def programmes(request, member):
    concerts = Concert.objects.filter(dateAndTime__lt=date.today()).order_by('dateAndTime').reverse()
    for concert in concerts:
        covers = glob.glob(
            settings.MEDIA_ROOT + "/programmes/KSO programme cover {0.dateAndTime:%Y%m%d}.jpg".format(concert))
        programmes = glob.glob(
            settings.MEDIA_ROOT + "/programmes/KSO programme {0.dateAndTime:%Y%m%d}.pdf".format(concert))
        if covers and programmes:
            concert.programme = (
                settings.MEDIA_URL + programmes[0][len(settings.MEDIA_ROOT) + 1:], getsize(programmes[0]),
                (settings.MEDIA_URL + covers[0][len(settings.MEDIA_ROOT) + 1:]))

    return render_to_response_with_extra_data(request, "programmes.html", {'concerts': concerts}, member)


def listen(request, member):
    soundClips = SoundClip.objects.order_by('-concertPiece__concert__dateAndTime', 'sequence')
    return render_to_response_with_extra_data(request, "listen.html", {'soundClips': soundClips}, member)