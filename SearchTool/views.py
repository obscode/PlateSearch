from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.db.models import Q
import re
from .models import Direct
import ephem
from astropy.coordinates import get_icrs_coordinates
from astropy.coordinates.name_resolve import sesame_database


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

def validate_field_list(arg):
   if len(arg) < 1:
      raise forms.ValidationError("You must choose at least one field to search")

def resolveName(name, database):
   sesame_database.set(database)
   #try:
   sky = get_icrs_coordinates(name)
   return sky.ra.value,sky.dec.value
   #except:
   #   return None,None

def index(request):
   return HttpResponse("This is a test of the emergency broadcasting service.")

def plate_view(request, plateid):
   plate = Direct.objects.get(pk=plateid)
   t = loader.get_template("SearchTool/plate_detail.html")
   c = {"plate":plate}
   return HttpResponse(t.render(c, request))

class SearchForm(forms.Form):
   search_type = forms.CharField(required=True, label="Search Type", initial="name",
      widget=forms.RadioSelect(choices=SEARCH_CHOICES))
   pattern_type = forms.CharField(required=True, label="Pattern Type",
      widget=forms.Select(choices=PATTERN_CHOICES))
   field_list = forms.MultipleChoiceField(required=False, initial=["object"],
         choices=FIELD_CHOICES, validators=[validate_field_list],
         widget=forms.CheckboxSelectMultiple())
   pattern = forms.CharField(required=False, label="Pattern:",
         widget=forms.TextInput(attrs={'size':'16'}))
   name = forms.CharField(required=False, label="Name:",
         widget=forms.TextInput(attrs={'size':'16'}))
   db_source = forms.CharField(required=True, label="Get Coords from", initial="NED",
         widget=forms.RadioSelect(choices=DB_CHOICES))
   ra = forms.CharField(required=False, label="RA",
         widget=forms.TextInput(attrs={'size':'10'}))
   dec = forms.CharField(required=False, label="DEC",
         widget=forms.TextInput(attrs={'size':'10'}))
   radius = forms.FloatField(required=False, label="Radius", initial=10.,
         widget=forms.TextInput(attrs={'size':'5'}))
   date_low = forms.DateField(required=False, 
         widget=forms.TextInput(attrs={'size':'10'}))
   date_high = forms.DateField(required=False,
         widget=forms.TextInput(attrs={'size':'10'}))
   telescope_list = forms.MultipleChoiceField(required=False, initial=[],
         choices=TEL_CHOICES, widget=forms.CheckboxSelectMultiple())

   def clean(self):
      '''Check some inter-field logic.'''
      if self.cleaned_data['search_type'] == 'pattern':
         if self.cleaned_data['pattern'] is None or self.cleaned_data['pattern'] == '':
            raise forms.ValidationError("You must supply a pattern to search")
         if self.cleaned_data['pattern_type'] == 'regexp':
            # Check to make sure it's a valid regexp
            try:
               pat = re.compile(self.cleaned_data['pattern'])
            except:
               raise forms.ValidationError("Pattern is not a valid regular expression")
      elif self.cleaned_data['search_type'] == 'coord':
         if self.cleaned_data['name']:
            # Check to see if we can find the object.
            ra,dec = resolveName(self.cleaned_data['name'], 
                                 self.cleaned_data['db_source'].lower())
            if ra is None or dec is None:
               raise forms.ValidationError("NED could not find object")
            self.cleaned_data['ra'] = ra
            self.cleaned_data['dec'] = dec
         elif self.cleaned_data['ra'] and self.cleaned_data['dec']:
            # Validate the RA
            if hms_pat.search(self.cleaned_data['ra']):
               self.cleaned_data['ra'] = ephem.hours(str(self.cleaned_data['ra']))*180./pi
            elif float_ra_pat.search(self.cleaned_data['ra']):
               self.cleaned_data['ra'] = float(self.cleaned_data['ra'])
            else:
               raise forms.ValidationError("RA is not in a recognized format")
          
            # Validate the DEC
            if dms_pat.search(self.cleaned_data['dec']):
               self.cleaned_data['dec'] = ephem.degrees(str(self.cleaned_data['dec']))*180./pi
            elif float_dec_pat.search(self.cleaned_data['dec']):
               self.cleaned_data['dec'] = float(self.cleaned_data['dec'])
            else:
               raise forms.ValidationError("DEC is not in a recognized format")

         else:
            raise forms.ValidationError("You must either supply an object name or coordinates")
         if not self.cleaned_data['radius']:
            raise forms.ValidationError("You must supply the search radius")
      else:
         pass

      return self.cleaned_data


def plate_search(request):
   if request.method == "POST":
      form = SearchForm(request.POST)

      if form.is_valid():
         search_type = form.cleaned_data.get('search_type',None)
         pattern_type = form.cleaned_data.get('pattern_type',None)
         db_source = form.cleaned_data.get('db_source', None)
         field_list = form.cleaned_data.get('field_list',None)
         pattern = str(form.cleaned_data.get('pattern', None))
         ra = form.cleaned_data.get('ra',None)
         dec = form.cleaned_data.get('dec',None)
         radius = form.cleaned_data.get('radius',None)
         date_low = form.cleaned_data.get('date_low',None)
         date_high = form.cleaned_data.get('date_high',None)
         # Now we need to convert the dates:
         if date_low is not None:  date_low = ephem.Date(date_low)
         if date_high is not None:  date_high = ephem.Date(date_high)
         telescope_list = form.cleaned_data.get('telescope_list',[])
  
         q = Direct.objects.all()    # This is lazy!  It hasn't happened yet
         # now since telescope and date filters are common to all, filter on this 
         #   first.
         if telescope_list:
            query = Q(telescope=telescope_list[0])
            for tel in telescope_list[1:]:
               query = query | Q(telescope=tel)
            q = q.filter(query)
         if date_low is not None:
            q = q.filter(date__gte=date_low)
         if date_low is not None:
            q = q.filter(date__lte=date_high)
 
         if search_type == "pattern":
            if pattern_type != 'regexp':
               # We can do this with built-in filters (faster)
               kwargs = {}
               for field in field_list:
                  field = str(field)
                  if pattern_type == 'exact':
                     kwargs["%s__iexact" % field] = pattern
                  elif pattern_type == 'startswith':
                     kwargs["%s__istartswith" % field] = pattern
                  elif pattern_type == 'endswith':
                     kwargs["%s__iendswith" % field] = pattern
                  elif pattern_type == 'contains':
                     kwargs["%s__icontains" % field] = pattern
               #print kwargs
               q = q.filter(**kwargs)
            else:
               # regexp, so need to do this the non-lazy way
               pat = re.compile(pattern)
               for field in field_list:
                  q = [obj for obj in q\
                        if obj.__dict__[field] is not None and\
                        pat.search(obj.__dict__[field])]
         elif search_type == 'coord':
            # do a coordinate search
            rad = radius/60.
            ra0 = ra-rad;  ra1 = ra + rad
            dec0 = dec-rad;  dec1 = dec+rad
            q = q.filter(ra__gte=ra0).filter(ra__lte=ra1)
            q = q.filter(decl__gte=dec0).filter(decl__lte=dec1)
         plate_list = q

         t = loader.get_template('SearchTool/plate_list.html')
         c = {'plate_list':plate_list }
         return HttpResponse(t.render(c, request))
      else:
         plate_list = None
         search_type=request.POST.get('search_type', 'name')
         db_source=request.POST.get('db_source', 'name')
   else:
      form = SearchForm()
      search_type = 'coord'
      pattern_type = 'exact'
      db_source = 'NED'
      plate_list = None

   t = loader.get_template('SearchTool/plate_search.html')
   c = {'form':form, 'search_type':search_type, 'db_source':db_source}
   return HttpResponse(t.render(c, request))