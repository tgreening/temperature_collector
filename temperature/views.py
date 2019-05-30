# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
from datetime import datetime, date
from dateutil import tz
from decimal import *

import json
import logging
import requests, json
from temperature.models import Probe, Reading, Counter
from django.core.cache import cache

def index(request):
    return HttpResponse("This is the temperature site")

@csrf_exempt
def reading(request, probe_name):
    logger = logging.getLogger(__name__)
    probe_lookup = get_object_or_404(Probe, name=probe_name)
    measurement = Reading(probe = probe_lookup, degrees = request.POST['degrees'], unit_of_measurement = request.POST['units'], created_date = datetime.now())
#    measurement.save()
    cache.set(probe_name, measurement, None)
    try: 
 #     logger.debug('Trying to create Counter...')
      counter, created = Counter.objects.get_or_create(page=1) 
      counter.count = counter.count + 1
      counter.save()
 #     logger.debug(counter.count)
      if (counter.count >= 12): 
        counter.count = 0
        counter.save()
 #       logger.debug('counter reset to %d' % counter.count)

      if (counter.count >= 9):
        message = "%s reported a temperature of %s%s" % (probe_name, request.POST['degrees'], request.POST['units'])
 
        data = json.dumps({'text':message,'username':'Temperature Collector'})
        headers = {'Content-Type': 'application/json'}
 
        # sending post request and saving response as response object
#        r = requests.post(url = "https://hooks.slack.com/services/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", data = data, headers = headers)
    except:
      log.debug("Unexpected error:", sys.exc_info()[0])
    return HttpResponse()


def latest(request, probe_name):
    logger = logging.getLogger(__name__)
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    try: 
      probe = Probe.objects.get(name=probe_name.lower())
#      logger.debug(probe.name)
      latest = cache.get(probe_name) # Reading.objects.filter(probe_id=probe.id).order_by("-created_date")[:1]
#      logger.debug(latest.created_date)
      formatted_datetime = latest.created_date.strftime("%-I:%M %p")
      logger.debug(latest.unit_of_measurement)
      response = "The latest reading from %s is %s%s at %s" % (probe.name, latest.degrees, latest.unit_of_measurement, formatted_datetime)
#      response = "The latest reading from %s is %s%s at %s" % (probe.name, "{:10.2f}".format(latest.degrees), latest.unit_of_measurement, formatted_datetime)
      logger.debug(response)
      #response = "The latest reading from cache for %s  is %s" % (probe_name, cache.get(probe_name)) 
    except ObjectDoesNotExist:
      response = "I couldn't find probe %s" % probe_name 
    return HttpResponse(response)

def average(request, probe_name):
    probe = Probe.objects.get(name=probe_name.lower())
    last_five = Reading.objects.filter(probe_id=probe.id).order_by("-created_date")[:4]
    total = float(0)
    for reading in last_five:
       total = total + reading.degrees
    return HttpResponse("The average for %s is %s" % (probe_name, "{:10.2f}".format(total/4)))

@csrf_exempt
def ga(request):
    logger = logging.getLogger(__name__)
    data = json.loads(request.body)
    logger.debug(data)
    logger.debug(data['queryResult']['parameters'])
    location = data['queryResult']['parameters']['location'].lower()
    logger.debug(location)
    text_to_say = ""
    try:
      probe = Probe.objects.get(name=location)
      logger.debug(probe)
 #     logger.debug(probe.name)
      latest = cache.get(probe.name) #Reading.objects.filter(probe_id=probe.id).order_by("-created_date")[:1]
#      logger.debug(latest.created_date)
      formatted_datetime = latest.created_date.strftime("%-I:%M %p")
      logger.debug(latest.unit_of_measurement)
      if latest.unit_of_measurement == 'F':
        scale = 'Fahrenheit'
      else:
        scale = 'Celsius'
      text_to_say = "%s reported a temperature of %s degrees %s at %s" % (probe.name, latest.degrees, scale, formatted_datetime)
      logger.debug(text_to_say)
      response = "{'payload':{'google': {'expectUserResponse': false, 'richResponse': {'items': [ { 'simpleResponse': { 'textToSpeech': '%s' } } ] } } } }'" % (text_to_say)
      logger.debug(response)
    except Probe.DoesNotExist:
      text_to_say = "I cannot find a probe named %s.  Please try again" % (probe.name)
      response = "{'payload':{'google': {'expectUserResponse': false, 'richResponse': {'items': [ { 'simpleResponse': { 'textToSpeech': '%s' } } ] } } } }'" % (text_to_say)
    except Exception as e:
      logger.debug(e)
      response = "{'payload':{'google': {'expectUserResponse': false, 'richResponse': {'items': [ { 'simpleResponse': { 'textToSpeech': 'An Error Occurred please contact the admin' } } ] } } } }'" 
    http_response =HttpResponse(response)
    http_response['Content-Type'] = 'application/json'
    return http_response

def slack(request): 
    logger = logging.getLogger(__name__)
    try:
      logger.debug('In slack...')
      counter, created  = Counter.objects.get_or_create(page=1) 
      logger.debug('Counter 1: %s' % counter)
      counter.count = counter.count + 1
      logger.debug('Counter 2: %d' % counter.count)
      if (counter.count >= 12): 
        counter.count = 0
      counter.save()
    except:
      log.debug("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(counter.count)
