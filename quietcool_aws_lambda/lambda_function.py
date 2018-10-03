#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
   AWS Lambda function to handle incoming requests from Alexa Skills Kit
   and update Thing Shadow for Quietcool fan controller
"""

import boto3
from enum import Enum
import json
import logging

from config import region_name, thing_name
from config import response_fallback, response_on, response_off
from config import response_fan_speed, response_error

# Initialize IoT client
client = boto3.client('iot-data', region_name=region_name)

class FanSpeed(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class FanPower(Enum):
    OFF = 0
    ON = 1

def switch_on_off_intent_handler(event,fan_power=FanPower.ON):

    # Pull back current shadow (for debugging)
    response = client.get_thing_shadow(thingName=thing_name)
    streamingBody = response["payload"]
    iot_shadow = json.loads(streamingBody.read())
    
    # Update thing shadow with new values
    data = {"state" : { "desired" : {"fan_power":fan_power.value}}}
    response = client.update_thing_shadow(
        thingName = thing_name, 
        payload = json.dumps(data)
    )
    streamingBody = response["payload"]
    iot_update = json.loads(streamingBody.read())

    if fan_power==FanPower.ON:
        return response_on
    elif fan_power==FanPower.OFF:
        return response_off
        
    return response_error
    
    
def fan_speed_intent_handler(event,fan_speed=FanSpeed.LOW):

    # Pull back current shadow (for debugging)
    response = client.get_thing_shadow(thingName=thing_name)
    streamingBody = response["payload"]
    iot_shadow = json.loads(streamingBody.read())
    
    # Update thing shadow with new values
    data = {"state" : { "desired" : {"fan_speed":fan_speed.value,"fan_power":FanPower.ON.value}}}
    response = client.update_thing_shadow(
        thingName = thing_name, 
        payload = json.dumps(data)
    )
    streamingBody = response["payload"]
    iot_update = json.loads(streamingBody.read())

    return "%s %s" % (response_fan_speed, str(fan_speed))

def fallback_intent_handler():
    responseText = response_fallback
    return responseText

def lambda_handler(event, context):
    
    logging.info(event['request'])
    
    responseText = ""
    # Parse incoming request from Alexa
    if event['request']['intent']['name'] == 'SwitchOnIntent':
        responseText = switch_on_off_intent_handler(event,fan_power=FanPower.ON)
    elif event['request']['intent']['name'] == 'SwitchOffIntent':
        responseText = switch_on_off_intent_handler(event,fan_power=FanPower.OFF)
    elif event['request']['intent']['name'] == 'LowFanSpeedIntent':
        responseText = fan_speed_intent_handler(event,fan_speed=FanSpeed.LOW)
    elif event['request']['intent']['name'] == 'MediumFanSpeedIntent':
        responseText = fan_speed_intent_handler(event,fan_speed=FanSpeed.MEDIUM)
    elif event['request']['intent']['name'] == 'HighFanSpeedIntent':
        responseText = fan_speed_intent_handler(event,fan_speed=FanSpeed.HIGH)
    else:
        # AMAZON.FallbackIntent
        responseText = fallback_intent_handler()
    
    response = {
        'version':'1.0',
        'response': {
            'outputSpeech':{
                'type':'PlainText',
                'text':responseText
            }
        }
    }
    
    return response


