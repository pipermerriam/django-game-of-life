# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'World'
        db.create_table('world_world', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='paused', max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='title', overwrite=False)),
        ))
        db.send_create_signal('world', ['World'])

        # Adding model 'Generation'
        db.create_table('world_generation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('generation', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('world', self.gf('django.db.models.fields.related.ForeignKey')(related_name='generations', to=orm['world.World'])),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('world', ['Generation'])

        # Adding model 'Cell'
        db.create_table('world_cell', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('generation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cells', to=orm['world.Generation'])),
            ('child', self.gf('django.db.models.fields.related.OneToOneField')(related_name='parent', unique=True, to=orm['world.Cell'])),
            ('is_alive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.IntegerField')()),
            ('long', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('world', ['Cell'])

    def backwards(self, orm):
        # Deleting model 'World'
        db.delete_table('world_world')

        # Deleting model 'Generation'
        db.delete_table('world_generation')

        # Deleting model 'Cell'
        db.delete_table('world_cell')

    models = {
        'world.cell': {
            'Meta': {'object_name': 'Cell'},
            'child': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'parent'", 'unique': 'True', 'to': "orm['world.Cell']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'generation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cells'", 'to': "orm['world.Generation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.IntegerField', [], {}),
            'long': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'world.generation': {
            'Meta': {'object_name': 'Generation'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'generation': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'world': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'generations'", 'to': "orm['world.World']"})
        },
        'world.world': {
            'Meta': {'object_name': 'World'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'paused'", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['world']