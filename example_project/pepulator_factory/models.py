from django.db import models

class Pepulator (models.Model):
    serial_number = models.IntegerField(primary_key=True)
    height = models.IntegerField()
    width = models.IntegerField()
    manufacture_date = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=32)
    
    distributed_by = models.ForeignKey('Distributor', null=True, 
                                       related_name='stock')

    def __unicode__(self):
        return u'Pepulator #%s' % self.serial_number
    
    @models.permalink
    def get_absolute_url(self):
        return ('pepulator_detail_view', [str(self.serial_number)])


class Knuckle (models.Model):
    hardness = models.FloatField()
    img_url = models.URLField()
    pepulator = models.ForeignKey('Pepulator', related_name='knuckles')
    
    def __unicode__(self):
        return u'Knuckle of hardness %.2f' % self.hardness


class Jamb (models.Model):
    power = models.FloatField()
    pepulator = models.ForeignKey('Pepulator', related_name='jambs')
    
    def __unicode__(self):
        return u'Jamb with power %.2f' % self.power


class Distributor (models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    capacity = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('distributor_detail_view', [self.name])
