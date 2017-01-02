from datetime import date
from operator import attrgetter
from django.db import models
import unicodedata

class Composer(models.Model):
    firstName = models.CharField("First name", max_length = 50)
    lastName = models.CharField("Last name", max_length = 50)
    lastNamePrefix = models.CharField("Prefix (e.g. 'von')", max_length = 10, null = True, blank = True)
    dateOfBirth = models.DateField("Born", null = True, blank = True)
    dateOfBirthYearOnly = models.BooleanField("DoB year only")
    dateOfDeath = models.DateField("Died", null = True, blank = True)
    dateOfDeathYearOnly = models.BooleanField("DoD year only")
    content = models.TextField(max_length = 4000, blank = True)

    def image(self):
        if self.image_set.count() > 0:
            return self.image_set.all()[0]
        return False

    class Meta:
        ordering = ('lastName',)

    def dates_string(self):
        if self.dateOfBirth is None: return u""
        if self.dateOfDeath is None: return u"b. {0.dateOfBirth.year}".format(self)
        return u"{0.dateOfBirth.year}-{0.dateOfDeath.year}".format(self)

    def __str__(self):
        if self.lastNamePrefix is not None:
            return u"{0.lastName}, {0.firstName} {0.lastNamePrefix}".format(self)
        return u"{0.lastName}, {0.firstName}".format(self)

    def __unicode__(self):
        if self.lastNamePrefix is not None:
            return u"{0.firstName} {0.lastNamePrefix} {0.lastName}".format(self)
        return u"{0.firstName} {0.lastName}".format(self)

    def conventional_name(self):
        if not self.dateOfDeath is None:
            return unicode(self.lastName)
        return unicode(self)

class Venue(models.Model):
    name = models.CharField(max_length = 50)
    website = models.CharField(max_length = 150, blank = True)
    postcode = models.CharField(max_length = 8)
    content = models.TextField(max_length = 4000, blank = True)

    def image(self):
        if self.image_set.count() > 0:
            return self.image_set.all()[0]
        return False

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Piece(models.Model):
    title = models.CharField(max_length = 250)
    shortTitle = models.CharField("Short title", max_length = 50, null = True, blank = True)
    composer = models.ForeignKey(Composer, related_name = "Composer")
    orchestration = models.CharField("Orchestration", max_length = 100, null = True, blank = True)
    duration = models.SmallIntegerField(null = True, blank = True)
    alternativeComposer = models.ForeignKey(Composer, related_name = "Alternative composer", null = True, blank = True)
    alternativeComposerDesignation = models.CharField("Alternative designation", max_length = 20, null = True, blank = True)
    content = models.TextField(max_length = 4000, blank = True)

    def image(self):
        if self.image_set.count() > 0:
            return self.image_set.all()[0]
        return False

    class Meta:
        ordering = ('composer','shortTitle')

    def display_title(self):
        return self.shortTitle or self.title

    def __str__(self):
        return u"{0}: {1}".format(self.composer.lastName, self.display_title())

    def __unicode__(self):
        return u"{0}: {1}".format(self.composer.lastName, self.display_title())

    def with_composer(self):
        return u"{0}: {1}".format(self.composer.conventional_name(), self.display_title())

class Season(models.Model):
    title = models.CharField(max_length = 50)
    startDate = models.DateField("Starts", null = True, blank = True)
    endDate = models.DateField("Ends", null = True, blank = True)
    content = models.TextField(max_length = 4000, blank = True)

    def concertsInOrder(self):
        return sorted(list(self.concert_set.all()), key=attrgetter("dateAndTime"))

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

class Conductor(models.Model):
    firstName = models.CharField("First name", max_length = 50)
    lastName = models.CharField("Last name", max_length = 50)
    content = models.TextField(max_length = 4000, blank = True)

    def image(self):
        if self.image_set.count() > 0:
            return self.image_set.all()[0]
        return False

    def full_name(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def appearancesInOrder(self):
        return sorted(list(self.concert_set.all()), key=attrgetter("dateAndTime"), reverse=True)

    def __str__(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def __unicode__(self):
        return u"{0.firstName} {0.lastName}".format(self)

class Instrument(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Soloist(models.Model):
    firstName = models.CharField("First name", max_length = 50)
    lastName = models.CharField("Last name", max_length = 50)
    instrument = models.ForeignKey(Instrument)
    content = models.TextField(max_length = 4000, blank = True)

    def image(self):
        if self.image_set.count() > 0:
            return self.image_set.all()[0]
        return False

    def full_name(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def appearancesInOrder(self):
        return sorted(list(self.concertpiecesoloist_set.all()), key=attrgetter("concertPiece.concert.dateAndTime"), reverse=True)

    def __str__(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def __unicode__(self):
        return u"{0.firstName} {0.lastName}".format(self)

class Charity(models.Model):
    name = models.CharField("Name", max_length = 100)
    website = models.CharField("Website", max_length = 150, null = True, blank = True)
    content = models.TextField(max_length = 4000, null = True, blank = True)

    def image(self):
        if self.image_set.count() > 0:
            return self.image_set.all()[0]
        return False

    def __str__(self):
        return u"{0.name}".format(self)

    def __unicode__(self):
        return u"{0.name}".format(self)

    class Meta:
        verbose_name_plural = "charities"

class Concert(models.Model):
    season = models.ForeignKey(Season)
    dateAndTime = models.DateTimeField("When")
    conductor = models.ForeignKey(Conductor)
    linkText = models.CharField("Link text", max_length = 100, blank = True)
    isFundraiser = models.BooleanField("Fundraiser?")
    venue = models.ForeignKey(Venue)
    content = models.TextField(max_length = 4000, blank = True)
    ticketLink = models.CharField("Ticket link", max_length = 150, blank = True)
    isSponsoredPlay = models.BooleanField("Sponsored play?")
    charity = models.ForeignKey(Charity, null = True, blank = True)

    def displayDescription(self):
        if self.dateAndTime.date() >= date(1955, 9, 1):
            return u"{0.dateAndTime:%d %B %Y}".format(self)
        return self.season.title

    def pageSubtitle(self):
        if self.dateAndTime.date() >= date(1955, 9, 1):
            return u"{0.dateAndTime:%I.%M%p, %A %d %B %Y}".format(self)
        return self.season.title

    def pageTitle(self):
        if self.dateAndTime.date() >= date(1955, 9, 1):
            return u"Concert on {0.dateAndTime:%d %B %Y}".format(self)
        return self.season.title

    def shouldDisplayVenue(self):
        if self.dateAndTime.date() >= date(1955, 9, 1):
            return True
        return False

    def image(self):
        image = False
        if self.charity:
            image = self.charity.image()
        if not image:
            for concertPiece in self.concertpiece_set.all():
                for soloist in concertPiece.concertpiecesoloist_set.all():
                    image = soloist.soloist.image()
                    if image: break
        if not image:
            if self.conductor.pk != 1:
                image = self.conductor.image()
        if not image:
            for concertPiece in self.concertpiece_set.all().order_by('sequence').reverse():
                image = concertPiece.piece.image()
                if image: break
        if not image:
            for concertPiece in self.concertpiece_set.all().order_by('sequence').reverse():
                image = concertPiece.piece.composer.image()
                if image: break
        if not image:
            if self.venue.image_set.all().count() > 0:
                image = self.venue.image()
        return image

    def link_url(self):
        return u"/concert/{0.pk}/".format(self)

    def toolTip(self):
        tt = u"KSO Concert::{0.venue.name}".format(self) + ":: "
        for piece in self.piecesInOrder():
            tt += u"::" + piece.piece.with_composer()
            if piece.comment:
                tt += u" (" + piece.comment + u")"
        return tt

    def piecesInOrder(self):
        return sorted(list(self.concertpiece_set.all()), key=attrgetter("sequence"))

    def dateAndVenue(self):
        return u"{0.dateAndTime:%d/%m/%Y} at {0.venue}".format(self)

    def description(self):
        return self.linkText or self.dateAndTime.strftime(u"%d/%m/%Y")

    def searchTerm(self):
        piece = self.concertpiece_set.latest(field_name='sequence').piece
        searchTerm = piece.composer.lastName + " " + piece.display_title()
        index = searchTerm.find('\'', 0)
        if index > 0:
            searchTerm = searchTerm[:index]
        index = searchTerm.find('"', 0)
        if index > 0:
            searchTerm = searchTerm[:index]
        return strip_accents(searchTerm).lower()

    def __str__(self):
        return self.description()

    def __unicode__(self):
        return self.description()

class Member(models.Model):
    firstName = models.CharField("First name", max_length = 50)
    lastName = models.CharField("Last name", max_length = 50)
    instrument = models.ForeignKey(Instrument)
    isPrincipal = models.BooleanField("Principal?")
    isFixer = models.BooleanField("Fixer?")
    firstConcert = models.ForeignKey(Concert, null = True, blank = True)
    content = models.TextField(max_length = 4000, blank = True)

    def full_name(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def __str__(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def __unicode__(self):
        return u"{0.firstName} {0.lastName}".format(self)

    def image(self):
        image = False
        for memberImage in self.image_set.all():
            image = memberImage
            if image: break
        return image

class ConcertPiece(models.Model):
    concert = models.ForeignKey(Concert)
    piece = models.ForeignKey(Piece)
    sequence = models.SmallIntegerField()
    isEncore = models.BooleanField()
    comment = models.CharField(max_length = 50, null = True, blank = True)

    def __str__(self):
        return u"{0.concert.dateAndTime:%d/%m/%Y}: {0.piece}".format(self)

    def __unicode__(self):
        return u"{0.concert.dateAndTime:%d/%m/%Y}: {0.piece}".format(self)

    def soloistsInOrder(self):
        return sorted(list(self.concertpiecesoloist_set.all()), key=attrgetter("sequence"))

    def soundClipsInOrder(self):
        return sorted(list(self.soundclip_set.all()), key=attrgetter("sequence"))

    class Meta:
        ordering = ["-concert__dateAndTime", "sequence"]

class SoundClip(models.Model):
    concertPiece = models.ForeignKey(ConcertPiece)
    sequence = models.SmallIntegerField()
    soundCloudEmbedCode = models.TextField(max_length = 1000)

    def __str__(self):
        return self.concertPiece.__str__;

    def __unicode__(self):
        return self.concertPiece.__unicode__;

class Rehearsal(models.Model):
    concert = models.ForeignKey(Concert)
    start = models.DateTimeField()
    end = models.DateTimeField()
    isSectional = models.BooleanField("Sectional")
    venue = models.ForeignKey(Venue)
    venueComment = models.TextField(max_length = 250, blank = True)
    altVenue = models.ForeignKey(Venue, null = True, blank = True)
    altVenueComment = models.TextField(max_length = 250, blank = True)
    content = models.TextField(max_length = 4000, blank = True)

    def link_url(self):
        return u"/concert/{0.concert.pk}/".format(self)

    def toolTip(self):
        tt = u"KSO Rehearsal::" + self.venue.name + ":: "
        for piece in self.concert.piecesInOrder():
            tt += u"::" + piece.piece.with_composer()
        for slot in self.rehearsalslot_set.order_by("start"):
            tt += u"::slot" + slot
        return tt

    def __str__(self):
        sectional_string = self.isSectional and u" (sectional)" or u""
        return u"{0.start:%d/%m/%Y}{1} at {0.venue}".format(self, sectional_string)

    def __unicode__(self):
        sectional_string = self.isSectional and u" (sectional)" or u""
        return u"{0.start:%d/%m/%Y}{1} at {0.venue}".format(self, sectional_string)

class RehearsalSlot(models.Model):
    rehearsal = models.ForeignKey(Rehearsal)
    start = models.DateTimeField()
    end = models.DateTimeField()
    concertPiece = models.ForeignKey(ConcertPiece)
    comment = models.CharField(max_length = 250, blank = True)

    def __str__(self):
        if self.comment:
            return u"{0.concertPiece} ({0.comment})".format(self)
        return unicode(self.concertPiece)

    def __unicode__(self):
        if self.comment:
            return u"{0.concertPiece} ({0.comment})".format(self)
        return unicode(self.concertPiece)

class SpecialPage(models.Model):
    name = models.CharField(max_length = 50)
    title = models.CharField(max_length = 150)
    menuKey = models.CharField(max_length = 20)
    content = models.TextField(max_length = 4000, blank = True)

    def menuIndex(self):
        if self.menuKey.isnumeric():
            return int(self.menuKey)
        return 0

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class ConcertPieceSoloist(models.Model):
    concertPiece = models.ForeignKey(ConcertPiece)
    soloist = models.ForeignKey(Soloist)
    sequence = models.SmallIntegerField()
    role = models.CharField(max_length = 50, null = True, blank = True)

    def __str__(self):
        return u"{0.soloist} ({0.concertPiece})".format(self)

    def __unicode__(self):
        return u"{0.soloist} ({0.concertPiece})".format(self)

    def displayRole(self):
        if self.role:
            return self.role
        return self.soloist.instrument.name

class Image(models.Model):
    caption = models.CharField("Caption", max_length = 100)
    fileName = models.FileField("Image file", upload_to="images")
    composer = models.ForeignKey(Composer, null = True, blank = True)
    venue = models.ForeignKey(Venue, null = True, blank = True)
    soloist = models.ForeignKey(Soloist, null = True, blank = True)
    conductor = models.ForeignKey(Conductor, null = True, blank = True)
    piece = models.ForeignKey(Piece, null = True, blank = True)
    charity = models.ForeignKey(Charity, null = True, blank = True)
    member = models.ForeignKey(Member, null = True, blank = True)
    isInGallery = models.BooleanField()
    credit = models.CharField("Credit", max_length = 200, null = True, blank = True)
    thumbnailName = models.FileField("Thumbnail file", upload_to="images", null = True, blank = True)

    def __str__(self):
        return self.caption

    def __unicode__(self):
        return self.caption

class SuggestedRepertoire(models.Model):
    piece = models.ForeignKey(Piece)
    #rating = RatingField(can_change_vote=True)
    content = models.TextField(max_length = 4000, blank = True)

    def __str__(self):
        return str(self.piece)

    def __unicode__(self):
        return unicode(self.piece)

def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

