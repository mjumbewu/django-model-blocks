from django.db import models

class PepulatorModel (models.Model):
    serial_number = models.IntegerField(primary_key=True)
    height = models.IntegerField()
    width = models.IntegerField()
    manufacture_date = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=32)
    
    distributed_by = models.ForeignKey('DistributorModel', null=True, 
                                       related_name='stock')

    def __unicode__(self):
        return u'Pepulator #%s' % self.serial_number
    
    @models.permalink
    def get_absolute_url(self):
        return ('pepulator_detail_view', [str(self.serial_number)])

class DistributorModel (models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    capacity = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('distributor_detail_view', [self.name])
