# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Pepulator'
        db.create_table('pepulator_factory_pepulator', (
            ('serial_number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('manufacture_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('distributed_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stock', null=True, to=orm['pepulator_factory.Distributor'])),
        ))
        db.send_create_signal('pepulator_factory', ['Pepulator'])

        # Adding model 'Distributor'
        db.create_table('pepulator_factory_distributor', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('pepulator_factory', ['Distributor'])


    def backwards(self, orm):
        
        # Deleting model 'Pepulator'
        db.delete_table('pepulator_factory_pepulator')

        # Deleting model 'Distributor'
        db.delete_table('pepulator_factory_distributor')


    models = {
        'pepulator_factory.distributor': {
            'Meta': {'object_name': 'Distributor'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'})
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
