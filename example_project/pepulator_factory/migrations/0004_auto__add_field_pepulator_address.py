# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Pepulator.address'
        db.add_column('pepulator_factory_pepulator', 'address', self.gf('django.db.models.fields.URLField')(max_length=200, null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Pepulator.address'
        db.delete_column('pepulator_factory_pepulator', 'address')


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
            'address': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'distributed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stock'", 'null': 'True', 'to': "orm['pepulator_factory.Distributor']"}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'manufacture_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['pepulator_factory']
