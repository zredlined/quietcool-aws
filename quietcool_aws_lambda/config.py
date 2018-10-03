#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
   Configuration settings for AWS Lambda handler
"""

# Settings
region_name = 'us-west-2'
thing_name = 'QuietcoolThing'

# Response texts
response_fallback = """I don't understand your request. You can say things such as: 
Alexa, ask house fan to turn on. Or, Alexa, ask house fan to set speed to medium."""

response_on = "I'll turn the house fan on"
response_off = "I'll turn the house fan off"
response_error = "Error: unknown intent"
response_fan_speed = "I'll set your fan speed to "
