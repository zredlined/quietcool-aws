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
#           "property":<INT VALUE>
#       }
#   }
# }

controller_url = "http://localhost:3001"
fan_ip = "10.0.11.100"
api_timeout = 5 # seconds
