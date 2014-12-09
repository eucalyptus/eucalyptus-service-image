#!/bin/sh
set -e

SERVICE_NAME=$1

# redirect STDERR to STDOUT and append (note the double >) both to /tmp/outfile
exec 1>> /var/log/eucalyptus-service-image.log 2>&1

yum -y --disablerepo \* --enablerepo eucalyptus-service-image install ${SERVICE_NAME}
service ${SERVICE_NAME} start
