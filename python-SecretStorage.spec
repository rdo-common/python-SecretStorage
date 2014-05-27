#global bzr     83
%global pkgname SecretStorage

Name:           python-%{pkgname}
Version:        2.0.0
%if 0%{?bzr}
Release:        0.2.bzr%{?bzr}%{?dist}
%else
Release:        2%{?dist}
%endif
Summary:        Python 2.x module for secure storing of passwords and secrets
URL:            http://launchpad.net/python-secretstorage
%if 0%{?bzr}
# Bazaar revision 83 snapshot downloaded at 2013-11-15 from launchpad via:
# bzr branch -r 83 lp:python-secretstorage python-secretstorage-bzr
# pushd python-secretstorage-bzr
# bzr export ../python-secretstorage-bzr83.tgz
# popd
Source0:        python-secretstorage-bzr%{bzr}.tgz
%else
Source0:        https://pypi.python.org/packages/source/S/%{pkgname}/%{pkgname}-%{version}.tar.gz
%endif
License:        BSD
BuildArch:      noarch
BuildRequires:  python-nose
BuildRequires:  python2-devel
# Building docs needed.
BuildRequires:  dbus-python
BuildRequires:  python-sphinx
# Tests only.
# Emulate the X environment.
# BuildRequires:  xorg-x11-server-Xvfb
# BuildRequires:  gnome-keyring
# BuildRequires:  python-crypto
Requires:       dbus-python

%description
This module provides a way for securely storing passwords and other secrets.

It uses D-Bus Secret Service API that is supported by GNOME Keyring (>= 2.30) 
and KSecretsService.

The main classes provided are secretstorage.Item, representing a secret item 
(that has a label, a secret and some attributes) and secretstorage.Collection,
a place items are stored in.

SecretStorage supports most of the functions provided by Secret Service, 
including creating and deleting items and collections, editing items, locking 
and unlocking collections (asynchronous unlocking is also supported).

%package -n     python3-%{pkgname}
Summary:        Python 3.x module for secure storing of passwords and secrets
BuildRequires:  python3-devel
BuildRequires:  python3-nose
# Tests only.
BuildRequires:  python3-dbus
Requires:       python3-dbus

%description -n python3-%{pkgname}
This module provides a way for securely storing passwords and other secrets.

It uses D-Bus Secret Service API that is supported by GNOME Keyring (>= 2.30) 
and KSecretsService.

The main classes provided are secretstorage.Item, representing a secret item 
(that has a label, a secret and some attributes) and secretstorage.Collection,
a place items are stored in.

SecretStorage supports most of the functions provided by Secret Service, 
including creating and deleting items and collections, editing items, locking 
and unlocking collections (asynchronous unlocking is also supported).

%package        doc
Summary:        Documentation for %{name}

%description    doc
Documentation for %{name}.

%prep
%if 0%{?bzr}
%setup -qn python-secretstorage-bzr%{bzr}
%else
%setup -qn %{pkgname}-%{version}
%endif
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
%{__python2} setup.py build
pushd %{py3dir}
%{__python3} setup.py build
popd
%{__python2} setup.py build_sphinx

%install
%{__python2} setup.py install --prefix=%{_prefix} -O1 --skip-build --root=%{buildroot}
pushd %{py3dir}
%{__python3} setup.py install --prefix=%{_prefix} -O1 --skip-build --root=%{buildroot}
popd
find %{_builddir} -name '.buildinfo' -delete -print

%check
#pushd tests
#PYTHONPATH=%{buildroot}%{python2_sitelib} xvfb-run -a %{__python2} -m unittest discover
#popd
#pushd %{py3dir}
#PYTHONPATH=%{buildroot}%{python3_sitelib} xvfb-run -a %{__python3} -m unittest discover
#popd

%files
%doc changelog LICENSE README*
%{python2_sitelib}/%{pkgname}-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/secretstorage/

%files -n python3-%{pkgname}
%doc changelog LICENSE README*
%{python3_sitelib}/%{pkgname}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/secretstorage/

%files doc
%doc build/sphinx/html/*

%changelog
* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Mar 30 2014 Christopher Meng <rpm@cicku.me> - 2.0.0-1
- Update to 2.0.0

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 1.1.0-1
- Update to 1.1.0

* Fri Nov 15 2013 Christopher Meng <rpm@cicku.me> - 1.0.0-0.3.bzr83
- Add license for doc package.
- Disable tests not runnable in Koji.

* Fri Nov 15 2013 Christopher Meng <rpm@cicku.me> - 1.0.0-0.2.bzr83
- Snapshot 83 rev to allow tests in mock.

* Tue Oct 22 2013 Christopher Meng <rpm@cicku.me> - 1.0.0-1
- Initial Package.
