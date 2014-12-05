#!/usr/bin/env python
#
# Copyright 2009-2013 Eucalyptus Systems, Inc.
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

from ConfigParser import ConfigParser as Config, NoOptionError
import optparse
import string
import sys

from jinja2 import Template


class MirrorConfig(Config):
    def __init__(self, config_file):
        if not isinstance(config_file, str):
            raise ArgumentError, "configuration file argument must be a string"
        Config.__init__(self)
        self.read(config_file)

    def get_repos(self, mirror_type):
        repos = []
        for repo in self.sections():
            try:
                if repo.split(':')[1] == mirror_type:
                    repo_entry = self._get_repo_entry(repo)
                    if repo_entry:
                        repos.append(repo_entry)
            except:
                pass
        return repos

    def _get_repo_entry(self, repo):
        repo_name = repo.split(':')[0]
        try:
            return (repo_name, 'baseurl', self.get(repo, 'baseurl'))
        except NoOptionError:
            try:
                return (repo_name, 'mirrorlist', self.get(repo, 'mirrorlist'))
            except NoOptionError:
                sys.stderr.write("-=[WARN]=- no valid url for repo '{}'\n".format(repo_name))
                return None
                

if __name__ == "__main__":
    usage = '%prog [-c config] [-m mirror_type] [template]'
    parser = optparse.OptionParser(usage=usage, version='%prog 0.1')
    parser.add_option('-c', '--config', default=None,
            help='template configuration options')
    parser.add_option('-m', '--mirror-type', default='public-nightly',
            help='choose configuration mirror type')
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error('must supply a kickstart template')
    if not opts.config:
        parser.error('mirror configuration file must be supplied')

    ks_template = args[0]
    mirror_config = MirrorConfig(opts.config)
    repos = mirror_config.get_repos(opts.mirror_type)

    if not repos:
        sys.stderr.write("-=[ERR]=- no repositories found\n")
        sys.exit(1)

    with open(ks_template) as ks_file:
        ks_string = Template(ks_file.read())
        print ks_string.render(repos=repos)

