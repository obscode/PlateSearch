from django import template
import re
from math import pi
import ephem

register = template.Library()

def NoneFilter(value):
   if value == "None" or value is None:
      return "&hellip;"
   else:
      return value
register.filter('NoneFilter',NoneFilter)

def date2hms(value):
   if value is None:  return('&hellip;')
   # assume it is a date object
   d = ephem.Date(value)
   return d.split()[1]
register.filter('date2hms',date2hms)

def date2ymd(value):
   if value is None:  return('&hellip;')
   d = ephem.Date(value).datetime()
   return "%04d/%02d/%02d" % (d.year,d.month,d.day)
register.filter('date2ymd',date2ymd)

def angle2hms(value):
   if value is None:  return('&hellip;')
   d = ephem.hours(value*pi/180.)
   return str(d)
register.filter('angle2hms',angle2hms)

def angle2dms(value):
   if value is None:  return('&hellip;')
   d = ephem.degrees(value*pi/180.)
   return(str(d))
register.filter('angle2dms',angle2dms)


def date2hm(value):
   if value is None:  return('&hellip;')
   d = ephem.Date(value)
   time = d.split()[1]
   #time = string.split(str(d))[1]
   return(":".join(time.split(":")[0:2]))
   #return(":".join(string.split(time,":")[0:2]))
register.filter('date2hm',date2hm)

def LST2hm(value):
   if value is None:  return('&hellip;')
   d = ephem.hours(value)
   return(":".join(d.split(":")[0:2]))
   #return(":".join(string.split(str(d),":")[0:2]))
register.filter('LST2hm',LST2hm)

def LST2hms(value):
   if value is None:  return('&hellip;')
   d = ephem.hours(value)
   return str(d)
register.filter('LST2hms',LST2hms)

def format(value,format):
   return format % value
register.filter('format',format)

def date2JD(value):
   return value + 2415020
register.filter('date2JD',date2JD)

def date2MJD(value):
   return value + 15019.5
register.filter('date2MJD',date2MJD)

def greek(value):
   '''Handle <Symbol stuff>'''
   greek = {'a':'&alpha;','D':'&Delta;','K':'&Kappa;','P':'&Pi;','H':'&Eta;',
      'p':'&pi;'}
   res = re.search(r'<font:Symbol>([a-zA-Z])(.*)',str(value))
   if not res:
      return str(value)
   ch = res.group(1)
   if ch in greek:
      return greek[ch]+res.group(2)
   else:
      return '<unknown symbol>'+res.group(2)
register.filter('greek',greek)

