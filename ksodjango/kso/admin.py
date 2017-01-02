from models import *
from django.contrib import admin
from markitup.widgets import AdminMarkItUpWidget


class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': AdminMarkItUpWidget}}


class PieceInline(admin.TabularInline):
    model = Piece
    fk_name = 'composer'
    exclude = ('content',)


class ComposerAdmin(MyModelAdmin):
    list_display = ('lastName', 'firstName', 'lastNamePrefix', 'dateOfBirth', 'dateOfDeath')
    list_display_links = ('lastName', 'firstName', 'lastNamePrefix', 'dateOfBirth', 'dateOfDeath')
    search_fields = ('lastName', 'firstName')
    inlines = (PieceInline,)
    ordering = ('lastName',)


class SoloistAdmin(MyModelAdmin):
    list_display = ('lastName', 'firstName', 'instrument')
    ordering = ('lastName',)


class RehearsalInline(admin.TabularInline):
    model = Rehearsal
    exclude = ('content',)


class ConcertPieceSoloistInline(admin.TabularInline):
    model = ConcertPieceSoloist


class ConcertPieceSoloistAdmin(admin.ModelAdmin):
    model = ConcertPieceSoloist


class ConcertPieceInline(admin.TabularInline):
    model = ConcertPiece
    inlines = (ConcertPieceSoloistInline,)


class ConcertPieceAdmin(admin.ModelAdmin):
    model = ConcertPiece
    inlines = (ConcertPieceSoloistInline,)


class SoundClipAdmin(admin.ModelAdmin):
    model = SoundClip


class ConcertAdmin(MyModelAdmin):
    list_display = ('dateAndTime', 'conductor', 'venue', 'linkText')
    list_display_links = ('dateAndTime', 'conductor', 'venue', 'linkText')
    inlines = (ConcertPieceInline, RehearsalInline,)
    ordering = ('-dateAndTime',)


class RehearsalSlotInline(admin.TabularInline):
    model = RehearsalSlot


class RehearsalAdmin(admin.ModelAdmin):
    inlines = (RehearsalSlotInline,)


class ConductorAdmin(MyModelAdmin):
    pass


class VenueAdmin(MyModelAdmin):
    list_display = ('name', 'website', 'postcode')
    list_display_links = ('name', 'website', 'postcode')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'composer', 'venue', 'soloist')
    list_display_links = ('caption',)
    ordering = ('caption',)


class SeasonAdmin(MyModelAdmin):
    list_display = ('title', 'startDate', 'endDate')
    list_display_links = ('title', 'startDate', 'endDate')
    ordering = ('-startDate',)


class SpecialPageAdmin(MyModelAdmin):
    list_display = ('name', 'title', 'menuKey')
    list_display_links = ('name', 'title', 'menuKey')
    ordering = ('name',)


admin.site.register(Concert, ConcertAdmin)
admin.site.register(Composer, ComposerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Instrument)
admin.site.register(Soloist, SoloistAdmin)
admin.site.register(Piece)
admin.site.register(Conductor, ConductorAdmin)
admin.site.register(ConcertPiece, ConcertPieceAdmin)
admin.site.register(SoundClip, SoundClipAdmin)
admin.site.register(ConcertPieceSoloist, ConcertPieceSoloistAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(SpecialPage, SpecialPageAdmin)
admin.site.register(Rehearsal, RehearsalAdmin)
admin.site.register(RehearsalSlot)
admin.site.register(Image)
admin.site.register(Charity)
admin.site.register(Member)