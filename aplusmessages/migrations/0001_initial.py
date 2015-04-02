# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SentMessage'
        db.create_table(u'aplusmessages_sentmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('from_email', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('recipient_type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('to_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cc_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bcc_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('html_body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('status_message', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'aplusmessages', ['SentMessage'])

        # Adding model 'Email'
        db.create_table(u'aplusmessages_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'aplusmessages', ['Email'])


    def backwards(self, orm):
        # Deleting model 'SentMessage'
        db.delete_table(u'aplusmessages_sentmessage')

        # Deleting model 'Email'
        db.delete_table(u'aplusmessages_email')


    models = {
        u'aplusmessages.email': {
            'Meta': {'object_name': 'Email'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'aplusmessages.sentmessage': {
            'Meta': {'object_name': 'SentMessage'},
            'bcc_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cc_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'html_body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'recipient_type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'status_message': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'to_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['aplusmessages']