# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Probe, Reading

admin.site.register(Probe)
admin.site.register(Reading)
