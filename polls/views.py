from django.shortcuts import get_object_or_404, render,get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import  Visitor, Plate

from django.db.models.functions import Length

import requests

from .forms import  VisitorForm, PlateForm

from django.shortcuts import redirect

from .helpers import *

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def add_entry():

    p=Plate(spz="NAME", cap_date=timezone.now(),image=None)
    save_image_from_url(p,'http://192.168.1.21:8080/shot.jpg')
    p.save()

def loaddb(request):
    print ("Saving")
    get_plates_from_spz_to_DB('http://spz.ditis.sk',100)
    plates_l = get_list_or_404(Plate)
    save_corrected_plates(plates_l)
    return render(request, 'polls/loaddb.html')

def show(request):
    print ("Saving")
    return render(request, 'polls/show.html')

def showPlates(request):

    plates_l = Plate.objects.annotate(text_len=Length('spz')).filter(text_len__gte=1)
    plates_l = plates_l.all().order_by('spz')
    #plates_l =get_list_or_404(Plate)
    #plates_l = plates_l.all().order_by('spz')

    return render(request, 'polls/showPlates.html',{'plates_l' : plates_l})

def showVisitors(request):
    visitors_l = get_list_or_404(Visitor)
    return render(request, 'polls/showVisitors.html',{'visitors_l' : visitors_l})

def showCorrected(request,pk):
    plate = get_object_or_404(Plate, pk=pk)
    corrected=do_opencv(plate)
    return render(request, 'polls/showCorrected.html',{'corrected' : corrected})

class HomePage(generic.TemplateView):
    template_name = 'polls/home.html'


def detail_visitor(request,spz):
    try:
        visitor = Visitor.objects.get(spz=spz)
        plates_l = Plate.objects.filter(visitor=visitor)

        all_plate=[]
        uvisitor = Visitor.objects.get(spz='BA000XX')
        all_plates = Plate.objects.filter(visitor=uvisitor)
        #all_plates = Plate.objects.all().exclude(spz=spz)
        for plate in all_plates:
            plate.similarity=similar(visitor.spz,plate.spz)
            plate.save()
        all_plates=all_plates.order_by('-similarity')
        for plate in all_plates:
            if plate.similarity > 0.5:
                all_plate.append(plate)
    except Visitor.DoesNotExist:
        visitor = Visitor.objects.get(spz='BA000XX')
        plates_l = Plate.objects.get(visitor=visitor)
        return render(request, 'polls/detail_visitor.html',{'visitor' : visitor})

    return render(request, 'polls/detail_visitor.html',{'visitor' : visitor , 'plates_l' : plates_l,'all_plate':all_plate,})

def visitor_new(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            print ("je valiad new")
            visitor = form.save(commit=False)
            visitor.reg_date = timezone.now()
            visitor.save()
            uvisitor= Visitor.objects.get(spz='BA000XX')
            plate_l = Plate.objects.filter(visitor=uvisitor)
            print(str(plate_l) + "pred IF")
            if plate_l.filter(spz=visitor.spz):
                for plate in plate_l.filter(spz=visitor.spz):
                    plate.visitor=visitor
                    plate.save()
                    print(str(plate) + "Prve for")
            if plate_l.filter(corrSpz=visitor.spz):
                for plate in plate_l.filter(corrSpz=visitor.spz):
                    plate.visitor=visitor
                    plate.save()
                    print(str(plate) + "Druhe for")



            return redirect('polls:detail_visitor', spz=visitor.spz)
    else:
        form = VisitorForm()
    return render(request, 'polls/visitor_edit.html', {'form': form})

def visitor_edit(request,spz):
    visitor = get_object_or_404(Visitor, spz=spz)
    if request.method == "POST":
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            print ("je valiad edit")
            visitor = form.save(commit=False)
            visitor.save()
            return redirect('polls:detail_visitor', spz=visitor.spz)
    else:
        form = VisitorForm(instance=visitor)
    return render(request, 'polls/visitor_edit.html', {'form': form})


###################################################chybovu hlasku ak PK neexistuje
def detail_plate(request,pk):
    try:
        plate = Plate.objects.get(pk=pk)
        if request.method == "POST":
            form = PlateForm(request.POST, instance=plate)
            form.fields['corrSpz'].required = False
            if form.is_valid():

                plate = form.save(commit=False)
                print (plate.corrSpz)
                try:
                    if plate.corrSpz=='':
                        visitor = Visitor.objects.get(spz=plate.spz)
                    else:
                        visitor = Visitor.objects.get(spz=plate.corrSpz)
                except Visitor.DoesNotExist:
                    visitor = Visitor.objects.get(spz='BA000XX')
                plate.visitor = visitor
                plate.save()
                return redirect('polls:detail_plate', pk=plate.pk)
        else:
            form = PlateForm(instance=plate)
        return render(request, 'polls/detail_plate.html', {'plate' : plate,'form': form})
    except Visitor.DoesNotExist:
        print('exce')


    #return render(request, 'polls/detail_plate.html',{'plate' : plate})
