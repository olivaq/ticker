# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('ticker_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ticker', ['Node'])

        # Adding model 'Link'
        db.create_table('ticker_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('src', self.gf('django.db.models.fields.related.ForeignKey')(related_name='next', to=orm['ticker.Node'])),
            ('dst', self.gf('django.db.models.fields.related.ForeignKey')(related_name='previous', to=orm['ticker.Node'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('debug', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ticker', ['Link'])

        # Adding model 'LinkDump'
        db.create_table('ticker_linkdump', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dumps', to=orm['ticker.Link'])),
            ('dump', self.gf('django.db.models.fields.TextField')()),
            ('result', self.gf('django.db.models.fields.TextField')()),
            ('rerun_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticker.LinkDump'])),
        ))
        db.send_create_signal('ticker', ['LinkDump'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table('ticker_node')

        # Deleting model 'Link'
        db.delete_table('ticker_link')

        # Deleting model 'LinkDump'
        db.delete_table('ticker_linkdump')


    models = {
        'ticker.link': {
            'Meta': {'object_name': 'Link'},
            'debug': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dst': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'previous'", 'to': "orm['ticker.Node']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'next'", 'to': "orm['ticker.Node']"})
        },
        'ticker.linkdump': {
            'Meta': {'object_name': 'LinkDump'},
            'dump': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dumps'", 'to': "orm['ticker.Link']"}),
            'rerun_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticker.LinkDump']"}),
            'result': ('django.db.models.fields.TextField', [], {})
        },
        'ticker.node': {
            'Meta': {'object_name': 'Node'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ticker']