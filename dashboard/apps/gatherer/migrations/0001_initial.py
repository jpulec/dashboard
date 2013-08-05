# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceGroup'
        db.create_table('gatherer_servicegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('environment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gatherer.Environment'])),
        ))
        db.send_create_signal('gatherer', ['ServiceGroup'])

        # Adding unique constraint on 'ServiceGroup', fields ['name', 'environment']
        db.create_unique('gatherer_servicegroup', ['name', 'environment_id'])

        # Adding model 'Environment'
        db.create_table('gatherer_environment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('gatherer', ['Environment'])

        # Adding model 'ServiceStatus'
        db.create_table('gatherer_servicestatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dttm', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('status_description', self.gf('django.db.models.fields.TextField')()),
            ('service_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gatherer.ServiceGroup'])),
        ))
        db.send_create_signal('gatherer', ['ServiceStatus'])

    def backwards(self, orm):
        # Removing unique constraint on 'ServiceGroup', fields ['name', 'environment']
        db.delete_unique('gatherer_servicegroup', ['name', 'environment_id'])

        # Deleting model 'ServiceGroup'
        db.delete_table('gatherer_servicegroup')

        # Deleting model 'Environment'
        db.delete_table('gatherer_environment')

        # Deleting model 'ServiceStatus'
        db.delete_table('gatherer_servicestatus')

    models = {
        'gatherer.environment': {
            'Meta': {'object_name': 'Environment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'gatherer.servicegroup': {
            'Meta': {'unique_together': "(('name', 'environment'),)", 'object_name': 'ServiceGroup'},
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gatherer.Environment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'gatherer.servicestatus': {
            'Meta': {'object_name': 'ServiceStatus'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'dttm': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gatherer.ServiceGroup']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'status_description': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['gatherer']