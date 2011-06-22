# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Knuckle.img_url'
        db.add_column('pepulator_factory_knuckle', 'img_url', self.gf('django.db.models.fields.URLField')(default='http://www.lllsoftware.it/Images/icoQuestion.png', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Knuckle.img_url'
        db.delete_column('pepulator_factory_knuckle', 'img_url')


    models = {
        'pepulator_factory.distributor': {
            'Meta': {'object_name': 'Distributor'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'})
        },
        'pepulator_factory.jamb': {
            'Meta': {'object_name': 'Jamb'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pepulator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jambs'", 'to': "orm['pepulator_factory.Pepulator']"}),
            'power': ('django.db.models.fields.FloatField', [], {})
        },
        'pepulator_factory.knuckle': {
            'Meta': {'object_name': 'Knuckle'},
            'hardness': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'pepulator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'knuckles'", 'to': "orm['pepulator_factory.Pepulator']"})
        },
        'pepulator_factory.pepulator': {
            'Meta': {'object_name': 'Pepulator'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'distributed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stock'", 'null': 'True', 'to': "orm['pepulator_factory.Distributor']"}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'manufacture_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['pepulator_factory']
