# prerequisites: for this script to work, install the following packages:
#
#  virt-install python-jinja2 python-jinja2-26 qemu-kvm libvirt createrepo libguestfs-tools rpm-build
#
# if building in Jenskins, comment out this:
export BUILD_NUMBER=007

export GIT_COMMIT_SHORT=`git rev-parse --short HEAD`
export GIT_COMMIT_COUNT="$(git log --pretty=format:'' HEAD | wc -l)"
if [ "$add_git_info" = "true" ]; then
    export BUILD_ID=$GIT_COMMIT_COUNT.$BUILD_NUMBER.$(date +%y%m%d)git${GIT_COMMIT_SHORT}
else
    export BUILD_ID=$GIT_COMMIT_COUNT.$BUILD_NUMBER
fi
export BASENAME=eucalyptus-service-image
if [ -z "$BUILD_VERSION" ]; then
    export BUILD_VERSION=0.0
fi
export KSFILE=$BASENAME.ks
export IMGFILE=$BASENAME.img
export BUILD_MIRROR_TYPE=internal-ci
export PKGNAME=$BASENAME-$BUILD_VERSION-$BUILD_ID

scripts/ksgen.py -m $BUILD_MIRROR_TYPE -c mirrors.cfg $KSFILE.in > $KSFILE

virsh destroy $KSFILE || true
virsh undefine $KSFILE || true

virt-install -n $KSFILE -r 1024 --vcpus=1 --accelerate -v --disk path=$IMGFILE,size=2 -l http://mirror.eucalyptus-systems.com/mirrors/centos/6.5/os/x86_64/ --initrd-inject=$KSFILE --extra-args \"ks=file:/$KSFILE\" --arch=x86_64 --force --graphics vnc,listen=0.0.0.0


while virsh list | grep $KSFILE;do echo "Waiting for vm to complete";sleep 30; done
virsh undefine $KSFILE || true

virt-sysprep -a $IMGFILE

tar -czvf $PKGNAME.tgz $IMGFILE

scripts/build-rpm.sh

createrepo --no-database results
