from django.db import models

# Create your models here.
class Direct(models.Model):
   plateid = models.BigIntegerField(primary_key=True)
   plate = models.CharField(max_length=60, blank=True)
   exp_num = models.CharField(max_length=30, blank=True)
   telescope = models.CharField(max_length=60, blank=True)
   observer = models.CharField(max_length=60, blank=True)
   assistant = models.CharField(max_length=60, blank=True)
   object = models.CharField(max_length=90, blank=True)
   ra = models.FloatField(null=True, db_column='RA', blank=True) # Field name made lowercase.
   decl = models.FloatField(null=True, db_column='DECL', blank=True) # Field name made lowercase.
   date = models.FloatField(null=True, blank=True)
   begin = models.FloatField(null=True, blank=True)
   end = models.FloatField(null=True, blank=True)
   total = models.CharField(max_length=60, blank=True)
   location = models.CharField(max_length=30, blank=True)
   size = models.CharField(max_length=30, blank=True)
   emulsion = models.CharField(max_length=60, blank=True)
   filter = models.CharField(max_length=30, blank=True)
   seeing = models.FloatField(null=True, blank=True)
   ha_end = models.FloatField(null=True, db_column='HA_end', blank=True) # Field name made lowercase.
   remarks = models.CharField(max_length=300, db_column='Remarks', blank=True) # Field name made lowercase.
   scanned = models.IntegerField(null=True, blank=True)
   num_plates = models.IntegerField(null=True, blank=True)
   source = models.CharField(max_length=60, blank=True)
   xls = models.CharField(max_length=150)
   sheet = models.CharField(max_length=60)
   row = models.IntegerField()
   raw_ra = models.CharField(max_length=45, db_column='raw_RA', blank=True) # Field name made lowercase.
   raw_dec = models.CharField(max_length=45, db_column='raw_DEC', blank=True) # Field name made lowercase.
   raw_date = models.CharField(max_length=45, blank=True)
   raw_size = models.CharField(max_length=30, blank=True)
   raw_ha_end = models.CharField(max_length=30, db_column='raw_HA_end', blank=True) # Field name made lowercase.
   raw_seeing = models.CharField(max_length=30, blank=True)
   raw_begin = models.CharField(max_length=45, blank=True)
   raw_end = models.CharField(max_length=45, blank=True)
   coor_source = models.CharField(max_length=60, blank=True)
   temp = models.CharField(max_length=300, blank=True)
   class Meta:
      db_table = u'direct'

   def __unicode__(self):
      return self.plate