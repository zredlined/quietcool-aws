#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
Quietcool AWS configuration
"""

# Shadow JSON schema:
#
# Name: QuietcoolThing 
# {
#   "state": {
#       "desired":{
#           "fan_power":<INT VALUE 0 (off) 1 (on)>,
#           "fan_speed":<INT VALUE 1 (low) 2 (medium) 3 (high)>
#       }
#   }
# }

# Controller type interface
controller_type = ['Quietcool'][0]

# Path to Node.js quietcool server controller
# https://github.com/stabbylambda/quietcool-server
# Handles COAP communication to wifi smart controller
controller_url = "http://localhost:3001" 

# Local IP address of quietcool fan being controlled
# https://quietcoolsystems.com/products/wi-fi-smart-control/
# Note: Use DHCP reservations on your router to ensure this does not change!
fan_ip = "10.0.11.100"

# Should never take more than 5 seconds to update FAN settings
api_timeout = 5 # seconds

