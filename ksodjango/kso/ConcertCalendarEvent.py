from datetime import timedelta
from iCalendar import ICalendarFeed
from kso.models import Rehearsal
from models import Concert


class KsoCalendarEvent(ICalendarFeed):
    def item_uid(self, item):
        if isinstance(item, Concert):
            return "http://www.kso.org.uk/concert/{0.pk}/".format(item)
        else:
            return "http://www.kso.org.uk/rehearsal/{0.pk}/".format(item)

    def item_start(self, item):
        if isinstance(item, Concert):
            return item.dateAndTime
        else:
            return item.start

    def item_end(self, item):
        if isinstance(item, Concert):
            return item.dateAndTime + timedelta(minutes=150)
        else:
            return item.end

    def item_location(self, item):
        return item.venue.name

    def item_summary(self, item):
        if isinstance(item, Concert):
            return u"KSO concert: {0}".format(item.description())
        else:
            return str(item)

    def item_description(self, item):
        if isinstance(item, Concert):
            concert = item
        else:
            concert = item.concert
        programme_items = [u"{0}: {1}".format(piece.piece.composer.conventional_name(), piece.piece)
                           for piece in concert.piecesInOrder()]
        programme = u"\n".join(programme_items)
        template = u"Kensington Symphony Orchestra concert at {0.venue}\n\nProgramme:\n{1}"
        if isinstance(item, Rehearsal):
            template = u"Rehearsal for " + template
        return template.format(concert, programme)


class SeasonCalendarEvent(KsoCalendarEvent):
    def __init__(self, season, member):
        self.season = season
        self.member = member

    def items(self):
        if self.member:
            events = list(self.season.concert_set.all())
            for concert in self.season.concert_set.all():
                events.extend(list(concert.rehearsal_set.all()))
            return events
        else:
            return self.season.concert_set.all()

    def item_filename(self):
        return u"KSO {0.season}.ics".format(self)


class ConcertCalendarEvent(KsoCalendarEvent):
    def __init__(self, concert, member):
        self.concert = concert
        self.member = member

    def items(self):
        if self.member:
            return [self.concert] + list(self.concert.rehearsal_set.all())
        else:
            return [self.concert]

    def item_filename(self):
        return u"KSO concert {0.concert.dateAndTime:%Y-%m-%d}.ics".format(self)