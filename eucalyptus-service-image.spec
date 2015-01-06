%{!?build_version: %global build_version 0}

Name:           eucalyptus-service-image%{?devbuild:-devel}
Version:        %{build_version}
Release:        0%{?build_id:.%build_id}%{?dist}
Summary:        Eucalyptus Service Image

Group:          Applications/System
# License needs to be the *distro's* license (Fedora is GPLv2, for instance)
License:        GPLv2
URL:            http://www.eucalyptus.com/
# Eustore image tarball
Source0:        %{name}-%{build_version}%{?build_id:-%build_id}.tgz
# Image's OS's license
Source1:        IMAGE-LICENSE
# Kickstart used to build the image
Source2:        %{name}.ks
# Installation script
Source3:        euca-install-imaging-worker
Source4:        euca-install-load-balancer

Requires: euca2ools >= 3.1.0
Requires: python-boto

%if 0%{!?devbuild:1}
Obsoletes:      eucalyptus-imaging-worker-image < 1.1
Obsoletes:      eucalyptus-load-balancer-image < 1.2
Provides:       eucalyptus-imaging-worker-image
Provides:       eucalyptus-load-balancer-image
%endif


%description
This package contains a machine image for use in Eucalyptus to
instantiate multiple internal services.


%prep
cp -p %{SOURCE1} %{SOURCE2} %{_builddir}

%build
# No build required

%install
install -m 755 -d $RPM_BUILD_ROOT%{_datarootdir}/%{name}
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{_datarootdir}/%{name}
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/usr/bin
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/usr/bin

%files
%defattr(-,root,root,-)
%doc IMAGE-LICENSE %{name}.ks
%{_datarootdir}/%{name}
/usr/bin/euca-install-imaging-worker
/usr/bin/euca-install-load-balancer

%changelog
* Fri Dec 05 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 0.1
- Created
