# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LinkDump.created'
        db.alter_column('ticker_linkdump', 'created', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'LinkDump.created'
        db.alter_column('ticker_linkdump', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dump': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dumps'", 'to': "orm['ticker.Link']"}),
            'rerun_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticker.LinkDump']", 'null': 'True', 'blank': 'True'}),
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