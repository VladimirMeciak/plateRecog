from django import forms
from .models import Visitor, Plate
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap3_datetime.widgets import DateTimePicker

class VisitorForm(forms.ModelForm):

    class Meta:
        model = Visitor
        fields = ('name', 'spz','comment','allowed_date_from','allowed_date_to','allowed_time_from','allowed_time_to','profile_image',)
        labels = {
        'name': 'Meno',
        'spz':'Spz',
        'comment':'Komentar',
        'profile_image':'Profilovy obrazok',
        'allowed_date_from':'Povolenie od datumu',
        'allowed_date_to':'Povolenie do datumu',
        'allowed_time_from':'Povolenie od casu',
        'allowed_time_to':'Povolenie do casu',
        }
        help_texts = {
        'name': 'Some useful help text.',
        'allowed_date_from': 'fromat 01.12.2000',
        'allowed_date_to': 'fromat 01.12.2000',
        'allowed_time_from': 'fromat 23:59',
        'allowed_time_to': 'fromat 23:59',
        }
        dateOptions = {
        'format': 'DD.MM.YYYY ',

        }
        timeOptions = {
        'format': 'HH:mm',
        'icons':{'date':'glyphicon glyphicon-time'}


        }
        widgets = {
            'allowed_date_from':DateTimePicker(options=dateOptions),
            'allowed_date_to':DateTimePicker(options=dateOptions),
            'allowed_time_from':DateTimePicker(options=timeOptions,icon_attrs= {'class': 'glyphicon glyphicon-time'}),
            'allowed_time_to':DateTimePicker(options=timeOptions,icon_attrs= {'class': 'glyphicon glyphicon-time'}),
            #'allowed_date_to': AdminDateWidget(),
        }

class PlateForm(forms.ModelForm):

    class Meta:
        model = Plate
        fields = ('corrSpz', )
        labels = {
        'corrSpz': 'Skutocna Spz',
        }
        help_texts = {
        'corrSpz': 'Tu mozes upravit zle rozoznanu SPZ',
        }
