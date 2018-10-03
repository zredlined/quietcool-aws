#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
   Connection functions for Quietcool whole house fans
"""
from enum import Enum
import logging
import json
import requests

from fan_controller import FanController
from config import api_timeout, controller_url, fan_ip

class FanSpeed(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class FanPower(Enum):
    OFF = 1
    ON = 2

class QuietcoolController(FanController):
    def __init__(self):
        logging.info("Initializing Quietcool controller")

        # Initialize defaults
        super().__init__()
        self.fan_power = FanPower.OFF.value
        self.fan_speed = FanSpeed.LOW.value
        self.fan_ip = fan_ip 
        self.fan_uid = self.get_uid(fan_ip)

    # Grab current settings from the controller and return as JSON
    def get_info(self, ip):

        fan_status = {}
        try:
            r = requests.get(controller_url+'/fans/%s' % (ip), timeout=api_timeout)
            fan_status = json.loads(r.text)
        except requests.exceptions.Timeout as e:
            logging.error("Timeout talking to controller: %s" % (e))
            pass

        return fan_status

    # Grab current uid (unique id for fan) from fan controller and return as string
    # Return 'unknown' if API call fails
    def get_uid(self, ip):

        fan_info = self.get_info(ip)
        uid = fan_info.get('fans',[{'id':{'uid':'unknown'}}])[0]['id']['uid']

        return uid

    def get_shadow(self, loop_count):
        shadow = {"state":{"desired":{}}}
        shadow['state']['desired']['fan_power'] = self.fan_power
        shadow['state']['desired']['fan_speed'] = self.fan_speed
        shadow['state']['desired']['loop_count'] = loop_count
        return shadow

    # Set the FAN speed
    def set_fan_speed(self, fan_speed):
        fan_status = {}
        try:
            r = requests.post(controller_url+'/fans/%s/%s/setCurrentSpeed' % (self.fan_ip, self.fan_uid), timeout=api_timeout, data={'speed':fan_speed})
            fan_status = json.loads(r.text)
        except requests.exceptions.Timeout as e:
            logging.error("Timeout talking to controller: %s" % (e))
            pass

        return fan_status

    # Set the FAN power
    def set_fan_power(self, fan_power='on'):
        fan_power = {}
        try:
            if fan_power == 'on':
                r = requests.post(controller_url+'/fans/%s/%s/power' % (self.fan_ip, self.fan_uid), timeout=api_timeout, data={'on':True})
                fan_power = json.loads(r.text)
            elif fan_power == 'off':
                r = requests.post(controller_url+'/fans/%s/%s/power' % (self.fan_ip, self.fan_uid), timeout=api_timeout, data={'off':True})
                fan_power = json.loads(r.text)
        except requests.exceptions.Timeout as e:
            logging.error("Timeout talking to controller: %s" % (e))
            pass

        return fan_power

