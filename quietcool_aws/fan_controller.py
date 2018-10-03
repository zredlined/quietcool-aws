#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
Connection functions for whole house fans
"""

import logging

class FanController(object):
    """
    Base class for fan interfaces (Quietcool)
    Sub classes need to override the get_readings() method
    """
    def __init__(self):
       logging.info("Initializing generic fan controller")

    # Grab any readings from the sensor and return as JSON
    # This method should be overridden and never called directly
    def get_info(self):
        logging.error("Generic info method should not be called directly")
        return NotImplemented
