#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
Quietcool AWS Shadow delta controller (for testing only!)
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import argparse
import requests

from fan_controller_quietcool import QuietcoolController
from config import controller_url, api_timeout
from config import fan_ip
from config import controller_type

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        logging.error("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("fan_power: " + str(payloadDict["state"]["desired"]["fan_power"]))
        print("fan_speed: " + str(payloadDict["state"]["desired"]["fan_speed"]))
        print("loop_count: " + str(payloadDict["state"]["desired"]["loop_count"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        logging.error("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
    if responseStatus == "timeout":
        logging.error("Delete request " + token + " time out!")
    if responseStatus == "accepted":
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~")
        logging.debug("Delete request with token: " + token + " accepted!")
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        logging.error("Delete request " + token + " rejected!")

def main():

    # Read in command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
    parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
    parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
    parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
    parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
    parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                        help="Use MQTT over WebSocket")
    parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="Bot", help="Targeted thing name")
    parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicShadowUpdater", help="Targeted client id")

    args = parser.parse_args()
    host = args.host
    rootCAPath = args.rootCAPath
    certificatePath = args.certificatePath
    privateKeyPath = args.privateKeyPath
    port = args.port
    useWebsocket = args.useWebsocket
    thingName = args.thingName
    clientId = args.clientId

    if args.useWebsocket and args.certificatePath and args.privateKeyPath:
        parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
        parser.error("Missing credentials for authentication.")
        exit(2)

    # Port defaults
    if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
        port = 443
    if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
        port = 8883

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Init AWSIoTMQTTShadowClient
    myAWSIoTMQTTShadowClient = None
    if useWebsocket:
        myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
        myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
        myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
        myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
        myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect to AWS IoT
    myAWSIoTMQTTShadowClient.connect()

    # Create a deviceShadow with persistent subscription
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

    # Delete shadow JSON doc
    deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

    # Update shadow in a loop
    loopCount = 0

    # Initialize fan controller interface
    fan_controller = QuietcoolController() if controller_type == "Quietcool" else None

    while True:
        fan_info = fan_controller.get_info(fan_ip)
        #print(json.dumps(fan_info,indent=2))
        shadow = fan_controller.get_shadow(loopCount)
        deviceShadowHandler.shadowUpdate(json.dumps(shadow), customShadowCallback_Update, 5)
        loopCount += 1
        time.sleep(2)

if __name__ == '__main__':
    main()
