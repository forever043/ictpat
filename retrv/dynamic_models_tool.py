# -*- coding: UTF-8 -*-
""" dynamic models """

from django.db import models
from django.contrib import admin
from django.db.models.signals import class_prepared

def create_dynamic_model(modelname, fields=None, options=None, admin_options={}, app_label='', module='',):
	class Meta:
		pass

	if app_label:
		setattr(Meta, 'app_label', app_label)

	if options is not None:
		for key, value in options.iteritems():
			setattr(Meta, key, value)

	attrs = {'__module__': module, 'Meta': Meta}
	if fields:
		attrs.update(fields)
	model = type(modelname, (models.Model,), attrs)

	# Create an Admin class if admin options were provided
	if admin_options is not None:
		class Admin(admin.ModelAdmin):
			pass
		for key, value in admin_options:
			setattr(Admin, key, value)
		admin.site.register(model, Admin)

	return model

