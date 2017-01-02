from django.shortcuts import get_object_or_404
from django.utils.datastructures import SortedDict
from kso.models import Member
from kso.otherViews import render_to_response_with_extra_data

def addSection(column, section, orchestra):
    if column not in orchestra:
        orchestra[column] = SortedDict({})
    principals = Member.objects.filter(instrument__name = section).filter(isPrincipal = True)
    rankAndFile = Member.objects.filter(instrument__name = section).filter(isPrincipal = False).order_by("lastName")
    if principals or rankAndFile:
        orchestra[column][section] = []
        for principal in principals:
            orchestra[column][section].append(principal)
        for member in rankAndFile:
            orchestra[column][section].append(member)

def members(request, member):
    orchestra = SortedDict({})
    addSection(1, "Violin", orchestra)
    addSection(2, "Viola", orchestra)
    addSection(2, "Cello", orchestra)
    addSection(2, "Double Bass", orchestra)
    addSection(3, "Flute", orchestra)
    addSection(3, "Piccolo", orchestra)
    addSection(3, "Oboe", orchestra)
    addSection(3, "Cor Anglais", orchestra)
    addSection(3, "Clarinet", orchestra)
    addSection(3, "Bass Clarinet", orchestra)
    addSection(3, "Bassoon", orchestra)
    addSection(3, "Contrabassoon", orchestra)
    addSection(4, "French Horn", orchestra)
    addSection(4, "Trumpet", orchestra)
    addSection(4, "Trombone", orchestra)
    addSection(4, "Bass Trombone", orchestra)
    addSection(4, "Tuba", orchestra)
    addSection(4, "Percussion", orchestra)
    return render_to_response_with_extra_data(request, "members.html", {'orchestra': orchestra}, member)

def memberDetail(request, member_id, member):
    memberObject = get_object_or_404(Member, pk = member_id)
    return render_to_response_with_extra_data(request, "memberdetail.html", {'memberObject' : memberObject, 'image' : memberObject.image()}, member)
