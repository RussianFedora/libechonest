Name:		libechonest
Version:	1.2.1
Release:	1%{?dist}.R
Summary:	C++ wrapper for the Echo Nest API

Group:		System Environment/Libraries
License:	GPLv2+
URL:		https://projects.kde.org/projects/playground/libs/libechonest
Source0:	http://pwsp.cleinias.com/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	pkgconfig(QtNetwork)
BuildRequires:	qjson-devel

## upstream patches
# fix reported version
Patch100: libechonest-1.2.1-version.patch


%description
libechonest is a collection of C++/Qt classes designed to make a developer's
life easy when trying to use the APIs provided by The Echo Nest.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%patch100 -p1 -b .version


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}


%clean
rm -rf $RPM_BUILD_ROOT


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion libechonest)" = "%{version}"
# The tests need active internet connection, which is not available
# in koji builds
#make test -C %%{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{_libdir}/libechonest.so.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/echonest/
%{_libdir}/libechonest.so
%{_libdir}/pkgconfig/libechonest.pc


%changelog
* Wed Nov 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-1
- Update to 1.2.1
- BR: pkgconfig(QtNetwork)

* Sat Oct 08 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.2.0-1
- Update to 1.2.0

* Fri Aug 19 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.9-1
- Update to 1.1.9

* Wed Jun 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.8-1
- 1.1.8
- track soname
- %%check: verify pkgconfig sanity

* Tue May 10 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.5-1
- Update to 1.1.5

* Sun Mar 27 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.4-1
- Update to 1.1.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.1-1
- Update to 1.1.1

* Mon Dec 20 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.0-1
- Initial Fedora package
