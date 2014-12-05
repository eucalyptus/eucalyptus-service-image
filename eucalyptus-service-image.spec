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

Requires: euca2ools >= 3.1.0
Requires: python-boto

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

%files
%defattr(-,root,root,-)
%doc IMAGE-LICENSE %{name}.ks
%{_datarootdir}/%{name}

%changelog
* Fri Dec 05 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 0.1-0
- Created

