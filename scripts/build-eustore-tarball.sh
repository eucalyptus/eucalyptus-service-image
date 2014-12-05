#!/bin/bash
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

set -x

if [ `id -u` -ne 0 ]; then
    echo "Error: must run as root" >&2
    exit 1
fi

. scripts/buildenv.sh

KSFILE=$1
MIRRORTYPE=$2

if [ -z $KSFILE ]; then
    echo "Error: must to provide a kickstart file" >&2
    exit 1
fi

[ -z $MIRRORTYPE ] && MIRRORTYPE=public-nightly

KSGENFILE=${KSFILE%.in}
BASENAME=${KSGENFILE%.ks}
PKGNAME=$BASENAME-$BUILD_VERSION-$BUILD_ID

#
# Inject mirrors into the kickstart template
scripts/ksgen.py -m $MIRRORTYPE -c mirrors.cfg $KSFILE > $KSGENFILE

if [ ! -d ./ami-creator ]; then
	git clone git://github.com/katzj/ami-creator.git
fi

mkdir -p ./tmp

./ami-creator/ami_creator/ami_creator.py \
	-c $KSGENFILE -t ./tmp \
	-n $PKGNAME -v -e || exit 1

mkdir -p $PKGNAME
mv *.img vmlinuz* $PKGNAME/
tar -czvf $PKGNAME.tgz $PKGNAME
