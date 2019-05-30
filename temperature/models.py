# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Probe(models.Model):
	name = models.CharField(max_length=25)
	created_date = models.DateTimeField(auto_now_add=True, blank=True)
	def __str__(self):
		return self.name

class Reading(models.Model):
	probe = models.ForeignKey(Probe, on_delete=models.CASCADE)
	degrees = models.FloatField()
	unit_of_measurement = models.CharField(max_length=2)
	created_date = models.DateTimeField(auto_now_add=True, blank=True)
	def __str__(self):
	  return "%s %d%s at %s" % (self.probe.name, self.degrees, self.unit_of_measurement, self.created_date)

class Counter(models.Model):
    count = models.IntegerField(default=0)
    page = models.IntegerField() # or any other way to identify
                                 # what this counter belongs to

