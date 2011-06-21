# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Jamb'
        db.create_table('pepulator_factory_jamb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('power', self.gf('django.db.models.fields.FloatField')()),
            ('pepulator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jambs', to=orm['pepulator_factory.Pepulator'])),
        ))
        db.send_create_signal('pepulator_factory', ['Jamb'])

        # Adding model 'Knuckle'
        db.create_table('pepulator_factory_knuckle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hardness', self.gf('django.db.models.fields.FloatField')()),
            ('pepulator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='knuckles', to=orm['pepulator_factory.Pepulator'])),
        ))
        db.send_create_signal('pepulator_factory', ['Knuckle'])


    def backwards(self, orm):
        
        # Deleting model 'Jamb'
        db.delete_table('pepulator_factory_jamb')

        # Deleting model 'Knuckle'
        db.delete_table('pepulator_factory_knuckle')


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
