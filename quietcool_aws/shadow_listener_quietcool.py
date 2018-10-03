#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Alex Watson
# Authors: Alex Watson <zredlined@gmail.com>
# All Rights Reserved

"""
Quietcool AWS Shadow delta listener
"""

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import argparse
import requests

from fan_controller_quietcool import QuietcoolController
from config import fan_ip

# Initialize Quietcool controller
quietcool = QuietcoolController()

# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    #print(responseStatus)
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("fan_power:" + str(payloadDict["state"]["fan_power"]))
    print("fan_speed:" + str(payloadDict["state"]["fan_speed"]))
    print("loop_count:" + str(payloadDict["state"]["loop_count"]))
    print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")
    print(json.dumps(payloadDict,indent=2))

    # Grab fan details
    #r = requests.get('http://localhost:3001/fans/%s' % (fan_ip))
    #fan_details = json.loads(r.text)
    fan_uid = quietcool.get_uid(fan_ip)
    print("fan_ip: %s fan_uid: %s" % (fan_ip, fan_uid))

    # Set fan speed 
    if payloadDict["metadata"]["fan_speed"]["timestamp"] == payloadDict["timestamp"]:
        fan_speed = int(payloadDict["state"]["fan_speed"])
        fan_status = quietcool.set_fan_speed(fan_speed)
        logging.debug(fan_status)

    # Power on fan 
    if payloadDict["metadata"]["fan_power"]["timestamp"] == payloadDict["timestamp"]:
        if payloadDict["state"]["fan_power"] == 1: 
            print("Received request to turn on quietcool fan")
            # Power on fan
            fan_status = quietcool.set_fan_power(fan_power='on')
            logging.debug(fan_status)

        elif payloadDict["state"]["fan_power"] == 0:
            print("Received request to turn off quietcool fan")
            # Power off fan
            fan_status = quietcool.set_fan_power(fan_power='off')
            logging.debug(fan_status)
         

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
    parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicShadowDeltaListener",
                        help="Targeted client id")

    # Configure settings based on command-line parameters
    args = parser.parse_args()
    host = args.host
    rootCAPath = args.rootCAPath
    certificatePath = args.certificatePath
    privateKeyPath = args.privateKeyPath
    port = args.port
    useWebsocket = args.useWebsocket
    thingName = args.thingName
    clientId = args.clientId

    # Using MQTT over Websocket requires AWS credential setup with IoT permissions
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

    # Listen on deltas
    deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)

    # Loop forever
    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()
