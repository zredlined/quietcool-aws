# Getting started with Lambda

To use this Lambda function, zip all of the files in this directory
into a zip file and upload via the Lambda console as a Python 3.6 runtime

## In the Lambda console, specify 
* Runtime: Python 3.6
* Handler: lambda_function.lambda_handler


## Runtime tests
Example request from Alexa Skills Kit passed to Lambda Function
Use this as an example "test event" for your Lambda function

### SwitchOffIntent
```
{
  "request": {
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.879752de-3bfd-4b80-b62f-c65ad501a2cf",
    "timestamp": "2018-10-02T21:50:55Z",
    "locale": "en-US",
    "intent": {
      "name": "SwitchOffIntent",
      "confirmationStatus": "NONE"
    }
  }
}
```

### SwitchOnIntent
```
{
  "request": {
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.879752de-3bfd-4b80-b62f-c65ad501a2cf",
    "timestamp": "2018-10-02T21:50:55Z",
    "locale": "en-US",
    "intent": {
      "name": "SwitchOnIntent",
      "confirmationStatus": "NONE"
    }
  }
}
```

### LowFanSpeedIntent
```
{
  "request": {
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.879752de-3bfd-4b80-b62f-c65ad501a2cf",
    "timestamp": "2018-10-02T21:50:55Z",
    "locale": "en-US",
    "intent": {
      "name": "LowFanSpeedIntent",
      "confirmationStatus": "NONE"
    }
  }
}
```



