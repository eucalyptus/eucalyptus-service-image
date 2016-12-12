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
# Please contact Eucalyptus Systems, Inc., 6750 Navigator Way, Goleta
# CA 93117, USA or visit http://www.eucalyptus.com/licenses/ if you need
# additional information or have any questions.

import sys
import subprocess
import os
from urlparse import urlparse
from boto.sts import STSConnection


class EsiBase(object):
    def __init__(self, args):
        self.vars = {}
        self.args = args
        def_region = os.getenv("AWS_DEFAULT_REGION")
        self.region = args.region if args.region is not None else 'localhost' if def_region is None else def_region
        self.debug = args.debug
        if self.debug:
            print "Using {0} region".format(self.region)
        self._load_vars()
        self._set_environment()


    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--region', metavar='REGION', help=('region '
                                                                'name to search when looking up config file data'))
        parser.add_argument('--debug', help='Show debugging output', action='store_true')
        parser.add_argument('-I', metavar='KEY_ID', help="user's access key id")
        parser.add_argument('-S', metavar='KEY', help="user's secret key id")
        parser.add_argument('--ec2_url', metavar='EC2_URL', help="URL to EC2 service")
        parser.add_argument('--t_url', metavar='TOKEN_URL', help="URL to TOKEN service")
        parser.add_argument('--cf_url', metavar='AWS_CLOUDFORMATION_URL', help="URL to CLOUDFORMATION service")
        parser.add_argument('--eb_url', metavar='EUCA_BOOTSTRAP_URL', help="URL to BOOTSTRAP service")
        parser.add_argument('--ep_url', metavar='EUCA_PROPERTIES_URL', help="URL to PROPERTIES service")
        parser.add_argument('--ec_path', metavar='EUCALYPTUS_CERT', help="Path to EUCALYPTUS certificate")
        parser.add_argument('--iam_url', metavar='AWS_IAM_URL', help="URL to IAM service")

    def get_sts_connection(self):
        token_url = urlparse(self.vars['TOKEN_URL'])
        STSConnection.DefaultRegionEndpoint = token_url.hostname
        port = token_url.port if token_url.port else 80
        return STSConnection(is_secure=False, port=port, path=token_url.path,
                             aws_access_key_id=self.get_env_var('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=self.get_env_var('AWS_SECRET_ACCESS_KEY'))

    def _set_environment(self):
        for i in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
            os.environ[i] = self.vars[i]

    def list_system_accounts(self):
        accounts = {}
        process = subprocess.Popen(['/usr/bin/euare-accountlist', '-U', self.vars['AWS_IAM_URL'],
                                    '-I', self.vars['AWS_ACCESS_KEY_ID'],
                                    '-S', self.vars['AWS_SECRET_ACCESS_KEY']],
                                   stdout=subprocess.PIPE)
        for line in process.stdout:
            split = line.strip().split(None, 1)
            if len(split) > 1 and (split[0].startswith('(eucalyptus)')
                                   or split[0].startswith('eucalyptus')):
                accounts[split[0]] = split[1]
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
        opts = vars(self.args)
        VAR_NAMES = {'EUCA_PROPERTIES_URL': 'ep_url',
                     'TOKEN_URL': 't_url',
                     'AWS_CLOUDFORMATION_URL': 'cf_url',
                     'EUCA_BOOTSTRAP_URL': 'eb_url',
                     'EUCALYPTUS_CERT': 'ec_path',
                     'AWS_IAM_URL': 'iam_url',
                     'AWS_ACCESS_KEY_ID': 'I',
                     'AWS_SECRET_ACCESS_KEY': 'S',
                     'EC2_URL': 'ec2_url'}
        for k, v in VAR_NAMES.items():
            if self.get_env_var(k) is None and v in opts:
                self.vars[k] = opts[v]
        if self.debug:
            print "Current settings {0}".format(self.vars)
        # time to check vars
        self.check_environment()
        # assume eucalyptus account since this is a system tool
        if self.get_env_var('EC2_USER_ID') is None:
            self.vars['EC2_USER_ID'] = self.list_system_accounts()['eucalyptus']

    @staticmethod
    def _check_binary(binary):
        try:
            with open(os.devnull, 'w') as nullfile:
                subprocess.call(binary, env=os.environ.copy(), stdout=nullfile)
        except OSError:
            print >> sys.stderr, "Error: cannot execute '{0}' binary.".format(" ".join(binary))
            print >> sys.stderr, "Make sure EUCALYPTUS path variable is exported."
            sys.exit(1)

    def check_environment(self):
        if self.vars["EC2_URL"] is None or \
                self.vars["AWS_ACCESS_KEY_ID"] is None or \
                self.vars["AWS_SECRET_ACCESS_KEY"] is None or \
                self.vars["AWS_IAM_URL"] is None:
            print >> sys.stderr, "Error: Unable to find EC2_URL, AWS_IAM_URL, " \
                                 "AWS_ACCESS_KEY_ID, or AWS_SECRET_ACCESS_KEY"
            print >> sys.stderr, "Make sure your environment is properly configured."
            sys.exit(1)

    def _set_property(self, property, value):
        cmd = ['/usr/bin/euctl', '-U', self.vars['EUCA_PROPERTIES_URL'],
               "{0}={1}".format(property, value)]
        try:
            subprocess.check_call(cmd)
        except (OSError, subprocess.CalledProcessError):
            print >> sys.stderr, "Error: failed to set property {0} to {1}".format(property, value)
            print >> sys.stderr, "To set it manually run this command:"
            print >> sys.stderr, " ".join(cmd)
            sys.exit(1)

    def _get_property(self, property):
        try:
            cmd = ['/usr/bin/euctl', '-U', self.vars['EUCA_PROPERTIES_URL'], property]
            out = subprocess.Popen(cmd, env=os.environ.copy(), stdout=subprocess.PIPE).communicate()[0]
            res = out.split()
            return res[2] if len(res) == 3 else None
        except OSError:
            print >> sys.stderr, "Error: failed to get property {0}.".format(property)
            sys.exit(1)

    def get_env_var(self, var):
        return self.vars[var] if var in self.vars else None
