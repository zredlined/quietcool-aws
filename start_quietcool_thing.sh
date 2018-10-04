# stop script on error
set -e

# Check to see if root CA file exists, download if not
if [ ! -f ./root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
fi

# install AWS Device SDK for Python if not already installed
#if [ ! -d ./aws-iot-device-sdk-python ]; then
#  printf "\nInstalling AWS SDK...\n"
#  git clone https://github.com/aws/aws-iot-device-sdk-python.git
#  pushd aws-iot-device-sdk-python
#  python setup.py install
#  popd
#fi

# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub iot thing application...\n"
python quietcool_aws/shadow_listener_quietcool.py \
    -e XXXXXXXXX-ats.iot.us-west-2.amazonaws.com \
    -r ./certs/root-CA.crt \
    -c ./certs/QuietcoolThing.cert.pem \
    -k ./certs/QuietcoolThing.private.key \
    -n QuietcoolThing \
    -id quietcool-thing-python-abacabb
