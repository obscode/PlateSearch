from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import re

hms_pat = re.compile(r'^[0-9]{1,2}[ :][0-9]{1,2}[ :][0-9]{1,2}(\.[0-9]*)?$')
dms_pat = re.compile(r'^[\+\-]?[0-9]{1,2}[ :][0-9]{1,2}[ :][0-9]{1,2}(\.[0-9]*)?$')
float_ra_pat = re.compile(r'^[0-9]{1,3}(\.[0-9]*)?$')
float_dec_pat = re.compile(r'^[\+\-]?[0-9]{1,2}(\.[0-9]*)?$')

SEARCH_CHOICES = (('coord','Coordinates'),
          ('pattern','Pattern'),
          ('all','Show All'))
PATTERN_CHOICES = (('exact','Exact Match'),
          ('contains','Contains'), 
          ('startswith','Starts With'),
          ('endswith','Ends with'), 
          ('regexp','Regular Expression'))
FIELD_CHOICES = (('object','Object Name'),
                 ('observer','Observer'),
                 ('assistant','Assistant'),
                 ('plate','Plate ID'),
                 ('remarks','Remarks'),
                 ('location','Location'))
TEL_CHOICES = (('Pal48','Palomar 48-inch Schmidt'),
               ('Pal60','Palomar 60-inch'),
               ('Pal200','Palomar 200-inch'),
               ('LCO100','LCO duPont'),
               ('LCO40','LCO Swope'),
               ('MW60','Mnt. Wilson 60-inch'),
               ('MW100','Mnt. Wilson 100-inch'))
DB_CHOICES = (('NED','NED'), ('SIMBAD','SIMBAD'))

def index(request):
   return HttpResponse("This is a test of the emergency broadcasting service.")