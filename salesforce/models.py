# django-salesforce
#
# by Phil Christensen
# (c) 2012 Working Today
# See LICENSE.md for details
#

"""
Django models for accessing Salesforce objects.

The Salesforce database is somewhat un-UNIXy or non-Pythonic, in that
column names are all in CamelCase. No attempt is made to work around this
issue, but normal use of `db_column` and `db_table` parameters should work.
"""

import logging, urllib

from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.sql import compiler

from salesforce.backend import base, manager
from salesforce import fields

log = logging.getLogger(__name__)

class SalesforceModelBase(ModelBase):
	def __new__(cls, name, bases, attrs):
		supplied_db_table = getattr(attrs.get('Meta', None), 'db_table', None)
		result = super(SalesforceModelBase, cls).__new__(cls, name, bases, attrs)
		if(models.Model not in bases and supplied_db_table is None):
			result._meta.db_table = name
		return result

class SalesforceModel(models.Model):
	"""
	Abstract model class for Salesforce objects.
	"""
	__metaclass__ = SalesforceModelBase
	_base_manager = objects = manager.SalesforceManager()
	
	class Meta:
		abstract = True
		managed = False
	
	Id = fields.SalesforceIdField(primary_key=True)
