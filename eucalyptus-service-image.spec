Name:           eucalyptus-service-image
Version:        1
Release:        0%{?dist}
Summary:        Eucalyptus Service Image

Group:          Applications/System
# License needs to be the *distro's* license (Fedora is GPLv2, for instance)
License:        GPLv2
URL:            http://www.eucalyptus.com/
BuildArch:      noarch

Source0:        %{name}-%{version}.tar.xz

BuildRequires:  /usr/bin/virt-install
BuildRequires:  /usr/bin/virt-sparsify
BuildRequires:  /usr/bin/virt-sysprep
BuildRequires:  python-devel

Requires:       euca2ools >= 3.3
Requires:       eucalyptus-admin-tools >= 4.2
Requires:       python-prettytable

Obsoletes:      eucalyptus-imaging-worker-image < 1.1
Obsoletes:      eucalyptus-load-balancer-image < 1.2
Provides:       eucalyptus-imaging-worker-image
Provides:       eucalyptus-load-balancer-image


%description
This package contains a machine image for use in Eucalyptus to
instantiate multiple internal services.


%prep
%setup -q


%build
%configure %{?configure_opts}
make


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc IMAGE-LICENSE
/usr/bin/esi-describe-images
/usr/bin/esi-install-image
/usr/bin/esi-manage-stack
%{python_sitelib}/esitoolsupport*
# Something else should probably own the service-images dir at some
# point, but we can deal with that later when we have more than one.
/usr/share/eucalyptus/service-images/%{name}-%{version}.tar.xz


%changelog
* Wed Feb 17 2016 Eucalyptus Release Engineering <support@eucalyptus.com>
- remove python 2.7 requirement

* Fri Feb  5 2016 Eucalyptus Release Engineering <support@eucalyptus.com>
- build Centos 7 image; sunset database server

* Mon Sep 28 2015 Eucalyptus Release Engineering <support@eucalyptus.com>
- Pulled in euca2ools 3.3 for euca-generate-environment-config

* Wed Aug 26 2015 Eucalyptus Release Engineering <support@eucalyptus.com>
- Use make instead of custom scripts

* Fri Apr 24 2015 Eucalyptus Release Engineering <support@eucalyptus.com>
- Use esi prefix for tools

* Fri Dec 05 2014 Eucalyptus Release Engineering <support@eucalyptus.com>
- Created
