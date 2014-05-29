# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'users_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('skin_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('skin_color', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal(u'users', ['UserProfile'])

        # Adding model 'Interest'
        db.create_table(u'users_interest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Product'])),
            ('set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Set'])),
            ('custom_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.CustomSet'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='p', max_length=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['Interest'])

        # Adding unique constraint on 'Interest', fields ['user', 'product']
        db.create_unique(u'users_interest', ['user_id', 'product_id'])

        # Adding unique constraint on 'Interest', fields ['user', 'set']
        db.create_unique(u'users_interest', ['user_id', 'set_id'])

        # Adding unique constraint on 'Interest', fields ['user', 'custom_set']
        db.create_unique(u'users_interest', ['user_id', 'custom_set_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Interest', fields ['user', 'custom_set']
        db.delete_unique(u'users_interest', ['user_id', 'custom_set_id'])

        # Removing unique constraint on 'Interest', fields ['user', 'set']
        db.delete_unique(u'users_interest', ['user_id', 'set_id'])

        # Removing unique constraint on 'Interest', fields ['user', 'product']
        db.delete_unique(u'users_interest', ['user_id', 'product_id'])

        # Deleting model 'UserProfile'
        db.delete_table(u'users_userprofile')

        # Deleting model 'Interest'
        db.delete_table(u'users_interest')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.interest': {
            'Meta': {'unique_together': "(('user', 'product'), ('user', 'set'), ('user', 'custom_set'))", 'object_name': 'Interest'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'custom_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.CustomSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Product']"}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Set']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserProfile']"})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'skin_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'skin_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'web.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'web.customset': {
            'Meta': {'object_name': 'CustomSet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Set']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.UserProfile']"})
        },
        u'web.product': {
            'Meta': {'object_name': 'Product'},
            'big_img_url': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brandname': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'capacity': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'discount_price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fit_skin_type': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maker': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'original_price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'small_img_url': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'video_img_url': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'web.set': {
            'Meta': {'object_name': 'Set'},
            'big_img_url': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'discount_difference': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'small_img_url': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['users']