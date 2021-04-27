# Deployment Documentation

This app has been deployed using the
[Amazon Lightstail](https://aws.amazon.com/lightsail/) service and can be
accessed at the following address:

https://teach-lmm.tgc5nisb4br4a.us-west-2.cs.amazonlightsail.com

It is deployed on a container service (Medium [2 GB RAM, 1 vCPUs] × 1 node) and
includes a public facing Nginx web server, which acts as a reverse proxy,
passing incoming connections to the Bokeh server. See the
[Bokeh documentation](https://docs.bokeh.org/en/latest/docs/user_guide/server.html#basic-reverse-proxy-setup)
for additional info about this configuration.

Assuming you have the required tools installed
([Docker](https://docs.docker.com/engine/install/),
[Docker compose](https://docs.docker.com/compose/install/),
the [AWS Command Line Interface (CLI) tool](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
and the [Lightsail Control (lightsailctl) plugin](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-install-software), the app can be deployed 
using the following commands:

```sh
# Create the container service (if it does not yet exist)
aws lightsail create-container-service \
--service-name teach-lmm \
--power medium \
--scale 1

# Build the container images
docker build -t bokeh-container ./myapp
docker build -t nginx-container ./nginx

# Push the images
aws lightsail push-container-image \
--service-name teach-lmm \
--label bokeh-container \
--image bokeh-container

aws lightsail push-container-image \
--service-name teach-lmm \
--label nginx-container \
--image nginx-container

# Create the deployment
aws lightsail create-container-service-deployment \
--service-name teach-lmm \
--containers file://containers.json \       # update image IDs
--public-endpoint file://public-endpoint.json
```