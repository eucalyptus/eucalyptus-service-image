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

import sys
import subprocess
import os
from urlparse import urlparse


class EsiBase(object):

    def __init__(self, region='localhost'):
        self.vars = {}
        self.region = region
        self._load_vars()
        self.check_environment()

    def list_system_accounts(self):
        accounts = {}
        process = subprocess.Popen(['/usr/bin/euare-accountlist',
                                    '-U', self.vars["AWS_IAM_URL"],
                                    '-I', self.vars["AWS_ACCESS_KEY_ID"],
                                    '-S', self.vars["AWS_SECRET_ACCESS_KEY"]],
                                   stdout=subprocess.PIPE)
        t = process.communicate()
        if process.returncode == 0:
            for account in t[0].split('\n'):
                a = account.split('\t')
                if len(a) == 2:
                    accounts[a[0]] = a[1]
        return accounts

    def _load_vars(self):
        EsiBase._check_binary(['euca-generate-environment-config'])
        process = subprocess.Popen(['euca-generate-environment-config', '--simple', '--region',
                                    self.region], stdout=subprocess.PIPE)
        t = process.communicate()
        if process.returncode == 0:
            for var in t[0].split('\n'):
                v = var.split("=")
                if len(v) == 2:
                    self.vars[v[0]] = v[1] if v[1] != '' else None

    @staticmethod
    def _check_binary(binary):
        try:
            with open(os.devnull, 'w') as nullfile:
                subprocess.call(binary, env=os.environ.copy(), stdout=nullfile)
        except OSError:
            print >> sys.stderr, "Error: cannot execute '{0}' binary.".format(" ".join(binary))
            print >> sys.stderr, "Make sure EUCALYPTUS path variable is exported."
            sys.exit(1)

    def _get_properties_url(self):
        url = urlparse(self.vars["EC2_URL"])
        port = url.port if url.port else 80
        return "{0}://{1}:{2}{3}".format(url.scheme, url.hostname, port, '/services/Properties')

    def check_environment(self):
        if self.vars["EC2_URL"] is None or \
                        self.vars["AWS_ACCESS_KEY_ID"] is None or \
                        self.vars["AWS_SECRET_ACCESS_KEY"] is None:
            print >> sys.stderr, "Error: Unable to find EC2_URL, AWS_ACCESS_KEY_ID, or AWS_SECRET_ACCESS_KEY"
            print >> sys.stderr, "Make sure your environment is properly configured."
            sys.exit(1)

    def _set_property(self, property, value):
        cmd = ['/usr/bin/euctl', '-U', self._get_properties_url(),
               '-I', self.vars["AWS_ACCESS_KEY_ID"],
               '-S', self.vars["AWS_SECRET_ACCESS_KEY"],
               "{0}={1}".format(property, value)]
        try:
            subprocess.check_call(cmd, env=os.environ.copy())
        except (OSError, subprocess.CalledProcessError):
            print >> sys.stderr, "Error: failed to set property {0} to {1}".format(property, value)
            print >> sys.stderr, "To set it manually run this command:"
            print >> sys.stderr, " ".join(cmd)
            sys.exit(1)

    def _get_property(self, property):
        try:
            cmd = ['/usr/bin/euctl', '-U', self._get_properties_url(),
                   '-I', self.vars["AWS_ACCESS_KEY_ID"],
                   '-S', self.vars["AWS_SECRET_ACCESS_KEY"],
                   property]
            out = subprocess.Popen(cmd, env=os.environ.copy(), stdout=subprocess.PIPE).communicate()[0]
            value = out.split()[-1]
            return value if value else None
        except OSError:
            print >> sys.stderr, "Error: failed to get property {0}.".format(property)
            sys.exit(1)

    def get_env_var(self, service):
        return self.vars[service] if service in self.vars else None