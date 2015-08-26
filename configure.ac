AC_INIT([eucalyptus-service-image], [0])

INSTALL_TREE=http://linux.mirrors.es.net/centos/6/os/x86_64/
BASE_MIRROR=${INSTALL_TREE}
UPDATES_MIRROR=http://linux.mirrors.es.net/centos/6/updates/x86_64/
EPEL_MIRROR=http://linux.mirrors.es.net/epel/6/x86_64/
EUCALYPTUS_MIRROR=http://downloads.eucalyptus.com/software/eucalyptus/4.1/rhel/6/x86_64/
EUCA2OOLS_MIRROR=http://downloads.eucalyptus.com/software/euca2ools/3.2/rhel/6/x86_64/

AC_ARG_WITH(install-tree,
    [  --with-install-tree=<dir>       the location of the install tree],
    [INSTALL_TREE="${withval}"])
AC_ARG_WITH(base-mirror,
    [  --with-base-mirror=<dir>        the location of the base OS mirror],
    [BASE_MIRROR="${withval}"])
AC_ARG_WITH(updates-mirror,
    [  --with-updates-mirror=<dir>     the location of the updates mirror],
    [UPDATES_MIRROR="${withval}"])
AC_ARG_WITH(epel-mirror,
    [  --with-epel-mirror=<dir>        the location of the EPEL mirror],
    [EPEL_MIRROR="${withval}"])
AC_ARG_WITH(eucalyptus-mirror,
    [  --with-eucalyptus-mirror=<dir>  the location of the Eucalyptus mirror],
    [EUCALYPTUS_MIRROR="${withval}"])
AC_ARG_WITH(euca2ools-mirror,
    [  --with-euca2ools-mirror=<dir>   the location of the euca2ools mirror],
    [EUCA2OOLS="${withval}"])

AC_PATH_PROG(TIMEOUT, timeout)
AC_PATH_PROG(VIRSH, virsh)
AC_PATH_PROG(VIRT_SYSPREP, virt-sysprep)
AC_PATH_PROG(VIRT_SPARSIFY, virt-sparsify)

AC_CONFIG_FILES([
    Makefile
    eucalyptus-service-image.ks
])
AC_SUBST(INSTALL_TREE)
AC_SUBST(BASE_MIRROR)
AC_SUBST(UPDATES_MIRROR)
AC_SUBST(EPEL_MIRROR)
AC_SUBST(EUCALYPTUS_MIRROR)
AC_SUBST(EUCA2OOLS_MIRROR)
AC_SUBST(TIMEOUT)
AC_SUBST(VIRSH)
AC_SUBST(VIRT_SYSPREP)
AC_SUBST(VIRT_SPARSIFY)
AC_OUTPUT
