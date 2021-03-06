# quietcool-aws
Project to connect Quietcool Stealth whole house-fan Wifi controller to AWS and Alexa

# Setup instructions
The setup instructions below get you up and running on a Raspberry Pi running Debian (NOOBS Raspbian)

## Install Node.js typescript Quietcool Server
This server talks to the Quietcool WiFi controller via COAP (constrained appliation protocol)

First, we need to setup Node.js on the Raspberry Pi
```
# Install node.js binaries for ARMv7 (confirm right distro with uname -m)
mkdir src; cd src;
wget https://nodejs.org/dist/v8.12.0/node-v8.12.0-linux-armv7l.tar.xz
tar -xJf node-v8.12.0-linux-armv7l.tar.xz
cd node-v8.12.0-linux-armv7l/
cp -Rf * /usr/local

sudo apt-get install nodejs, npm
sudo npm install ts-node -g
```
Install the quietcool-server
```
cd ..;mkdir dev;cd dev;mkdir js; cd js
git clone https://github.com/stabbylambda/quietcool-server.git
cd quietcool-server
sudo npm install
echo "ts-node ./src/index.ts" > start.sh
sudo chmod u+x start.sh
```

Setup and install quietcool-aws
```
cd ../..;mkdir python3;cd python3
git clone https://github.com/zredlined/quietcool-aws
cd quietcool-aws
mkdir certs # copy your thing certificates from AWS and the root-CA.crt here
```

## Launch Quietcool-AWS 
(Ensure your certificate/IoT thing have appropriate IoT permissions)
`pip3 install -r requirements.txt`
```
printf "\nRunning pub/sub iot thing application...\n"
python3 quietcool_aws/shadow_listener_quietcool.py \
    -e XXXXXXXX-ats.iot.us-west-2.amazonaws.com \
    -r ./certs/root-CA.crt \
    -c ./certs/QuietcoolThing.cert.pem \
    -k ./certs/QuietcoolThing.private.key \
    -n QuietcoolThing \
    -id quietcool-thing-python-abacabb
```

Interested in testing updates live before connecting to Alexa?
```printf "\nRunning pub/sub controller application...\n"
python quietcool_aws/shadow_controller_quietcool.py \
    -e XXXXXXXXX-ats.iot.us-west-2.amazonaws.com \
    -r ./certs/root-CA.crt \
    -c ./certs/QuietcoolThing.cert.pem \
    -k ./certs/QuietcoolThing.private.key \
    -n QuietcoolThing \
    -id quietcool-controller-python-abacabb
```

## Install Quietcool-server and Quietcool-AWS as services on Raspberry Pi

### Create a systemctl service for the Quietcool AWS IoT Core Python client

`sudo vi /etc/systemd/system/quietcool-aws.service`

Copy in the following text (and modify AWS endpoint to match your IoT Core endpoint =)

```
[Unit]
Description=Quietcool AWS server
After=multi-user.target

[Service]
Type=simple
Restart=always
RestartSec=3
User=pi
WorkingDirectory=/home/pi/dev/python3/quietcool-aws/
ExecStart=/usr/bin/python3 /home/pi/dev/python3/quietcool-aws/quietcool_aws/shadow_listener_quietcool.py \
    -e XXXXXXXX-ats.iot.us-west-2.amazonaws.com \
    -r ./certs/root-CA.crt \
    -c ./certs/QuietcoolThing.cert.pem \
    -k ./certs/QuietcoolThing.private.key \
    -n QuietcoolThing \
    -id quietcool-thing-python-abacabb

[Install]
WantedBy=multi-user.target
```
### Create a systemctl service for the Quietcool COAP server (Node.js Typescript)
`sudo vi /etc/systemd/system/quietcool-aws.service`

Copy in the following text

```
[Unit]
Description=Quietcool COAP server
After=multi-user.target

[Service]
Type=simple
Restart=always
RestartSec=3
User=pi
WorkingDirectory=/home/pi/dev/js/quietcool-server/
ExecStart=/usr/local/bin/ts-node /home/pi/dev/js/quietcool-server/src/index.ts

[Install]
WantedBy=multi-user.target
```

### Set permissions to initialize each service on startup as systemctl daemons
```
# setup quietcool aws
sudo chmod 644 /etc/systemd/system/quietcool-aws.service
chmod +x /home/pi/dev/python3/quietcool-aws/quietcool_aws/shadow_listener_quietcool.py
sudo systemctl daemon-reload
sudo systemctl enable quietcool-aws.service
sudo systemctl start quietcool-aws.service
sudo systemctl status quietcool-aws.service

# setup quietcool coap
sudo chmod 644 /etc/systemd/system/quietcool-service.service
chmod +x /home/pi/dev/js/quietcool-server/src/index.ts
sudo systemctl daemon-reload
sudo systemctl enable quietcool-service.service
sudo systemctl start quietcool-service.service
sudo systemctl status quietcool-service.service
```

# Setting up your Alexa application using Alexa Skills Kit
Instructions comming soon!








