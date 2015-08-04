# Copyright 2009-2015 Eucalyptus Systems, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
# Please contact Eucalyptus Systems, Inc., 6755 Hollister Ave., Goleta
# CA 93117, USA or visit http://www.eucalyptus.com/licenses/ if you need
# additional information or have any questions.

#
# Order matters here. We want to make sure we initialize logging before anything
# else happens. We need to initialize the logger that boto will be using.
#

import euca2ools
import sys
import subprocess
import os
from urlparse import urlparse

(major, minor, patch) = euca2ools.__version__.split('-')[0].split('.')
if int(major) < 3 or (int(major) >= 3 and int(minor) < 1):
    print >> sys.stderr, "euca2ools version 3.1.0 or newer required."
    sys.exit(1)


def list_system_accounts():
    accounts = {}
    process = subprocess.Popen(['/usr/bin/euare-accountlist'], stdout=subprocess.PIPE)
    t = process.communicate()
    if process.returncode == 0:
        for account in t[0].split('\n'):
            a = account.split('\t')
            if len(a) == 2:
                accounts[a[0]] = a[1]
    return accounts


def _check_binary(binary):
    try:
        with open(os.devnull, 'w') as nullfile:
            subprocess.call(binary, env=os.environ.copy(), stdout=nullfile)
    except OSError:
        print >> sys.stderr, "Error: cannot find '{0}' binary.".format(binary)
        print >> sys.stderr, "Make sure EUCALYPTUS path variable is exported."
        sys.exit(1)


def _get_properties_url():
    url = urlparse(os.environ.get("EC2_URL"))
    p = url.path.split('/')
    p[len(p)-1] = 'Properties'
    port = url.port if url.port else 80
    return "{0}://{1}:{2}{3}".format(url.scheme, url.hostname, port, '/'.join(p))


def check_environment():
    if not "EC2_URL" in os.environ.copy():
        print >> sys.stderr, "Error: Unable to find EC2_URL"
        print >> sys.stderr, "Make sure your eucarc is sourced."
        sys.exit(1)
    for b in ['/usr/bin/euare-accountlist', '/usr/bin/euctl']:
        _check_binary(b)


def set_property(property, value):
    cmd = ['/usr/bin/euctl', '-U', _get_properties_url(), "{0}={1}".format(property, value)]
    try:
        subprocess.check_call(cmd, env=os.environ.copy())
    except (OSError, subprocess.CalledProcessError):
        print >> sys.stderr, "Error: failed to set property {0} to {1}".format(property, value)
        print >> sys.stderr, "To set it manually run this command:"
        print >> sys.stderr, " ".join(cmd)
        sys.exit(1)


def get_property(property):
    try:
        cmd = ['/usr/bin/euctl', '-U', _get_properties_url(), property]
        out = subprocess.Popen(cmd, env=os.environ.copy(), stdout=subprocess.PIPE).communicate()[0]
        value = out.split()[-1]
        if value == "NULL":
            return None
        else:
            return value
    except OSError:
        print >> sys.stderr, "Error: failed to get property {0}.".format(property)
        sys.exit(1)