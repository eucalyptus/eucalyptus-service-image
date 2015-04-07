%{!?build_version: %global build_version 0}

Name:           eucalyptus-service-image
Version:        %{build_version}
Release:        0%{?build_id:.%build_id}%{?dist}
Summary:        Eucalyptus Service Image

Group:          Applications/System
# License needs to be the *distro's* license (Fedora is GPLv2, for instance)
License:        GPLv2
URL:            http://www.eucalyptus.com/

Source0:        %{name}-%{build_version}%{?build_id:-%build_id}.tgz
# euimage metadata
# Source1:        %{name}.yml
# Image's OS's license
Source2:        IMAGE-LICENSE
# Kickstart used to build the image (included as documentation)
Source3:        %{name}.ks
# Describe images tool
Source4:        euca-describe-service-images
# Install tool
Source5:        euca-install-service-image

# BuildRequires:  euca2ools >= 3.2

Requires: python-prettytable

Obsoletes:      eucalyptus-imaging-worker-image < 1.1
Obsoletes:      eucalyptus-load-balancer-image < 1.2
Provides:       euclayptus-imaging-worker-image
Provides:       euclayptus-load-balancer-image
Provides:       euclayptus-database-server-image


%description
This package contains a machine image for use in Eucalyptus to
instantiate multiple internal services.

%prep
cp -p %{SOURCE2} %{SOURCE3} %{_builddir}

%build
# Dont use euimage-pack yet
# euimage-pack-image %{SOURCE0} %{SOURCE1}


%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/eucalyptus/service-images
install -m 644 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/eucalyptus/service-images/%{name}.tgz
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/usr/bin
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT/usr/bin


%files
%defattr(-,root,root,-)
%doc IMAGE-LICENSE %{name}.ks
# Something else should probably own the service-images dir at some
# point, but we can deal with that later when we have more than one.
/usr/share/eucalyptus/service-images/%{name}.tgz
/usr/bin/euca-describe-service-images
/usr/bin/euca-install-service-image

%changelog
* Fri Dec 05 2014 Eucalyptus Release Engineering <support@eucalyptus.com> - 0.1-0
- Created
