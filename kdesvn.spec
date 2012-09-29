# norootforbuild
Summary:   A subversion client for the KDE with KIO integration.
Name:      kdesvn
Version:   1.6.0
Release:   1%{?dist}
License:   LGPL
Vendor:    Rajko Albrecht <ral@alwins-world.de>
Url:       http://kdesvn.alwins-world.de
Group:     Development/Tools
Source:    kdesvn-%version.tar.bz2
BuildRoot: %{_tmppath}/%{name}-root
Requires: subversion >= 1.6.0
Requires: /usr/bin/dot
BuildRequires: cmake >= 2.4
BuildRequires: gcc-c++
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: subversion-devel >= 1.6.0
BuildRequires: kdelibs-devel >= 4.1

%description
Kdesvn is a subversion client for KDE.
It may used as standalone application or plugin (KPart). Base functions are provided
via a KIO protocol, too.

%package kiosvn
Requires: kdesvn = %{version}
Group:    Development/Tools
Summary:  A kde-kio integration for subversion based on kdesvn

%description kiosvn
KIO integration (KIO::svn) based on kdesvn alternative protocol name.

%package devel
Group:    Development/Libraries
Summary:  Wrapper lib for subversion QT integration.
Requires: subversion-devel >= 1.3.0
Requires: kdesvn = %{version}

%description devel
Development files for kdesvn.

%prep
%setup -q
mkdir build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=`kde-config --prefix` -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLIB_SUFFIX=`kde-config --libsuffix`

%build
cd build
# Setup for parallel builds
numprocs=`egrep -c ^cpu[0-9]+ /proc/stat || :`
if [ "$numprocs" = "0" ]; then
  numprocs=1
fi

make -j$numprocs

%install
cd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
gzip $RPM_BUILD_ROOT/%{_datadir}/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT/*
rm -rf $RPM_BUILD_DIR/kdesvn


%files
%defattr(-,root,root)
%{_bindir}/kdesvn
%{_bindir}/kdesvnaskpass
%{_libdir}/*/*part*
%{_datadir}/applications/*
%{_datadir}/kde4/apps/kdesvn/*
%{_datadir}/kde4/apps/kdesvnpart/*
%{_datadir}/kde4/apps/kconf_update/*
%{_datadir}/config.kcfg/*
%{_datadir}/doc/*
%{_datadir}/icons/*
%{_datadir}/locale/*
%{_libdir}/*/kded_kdesvnd.*
%{_datadir}/kde4/services/kded/kdesvnd.desktop
%{_datadir}/kde4/services/ServiceMenus/kdesvn*
%{_datadir}/kde4/services/kdesvnpart.desktop
%{_libdir}/*/kio_ksvn*
%{_datadir}/kde4/services/ksvn*.protocol
%{_datadir}/man/man1/*
%{_datadir}/dbus-1/interfaces/org.kde.kdesvnd.xml
%{_libdir}/libsvnqt.so*
%{_datadir}/svnqt/*
%doc AUTHORS ChangeLog GPL.txt TODO COPYING COPYING.OpenSSL

%files kiosvn
%defattr(-,root,root)
%{_datadir}/kde4/services/svn*.protocol

%files devel
%defattr(-,root,root)
%dir %{_includedir}/svnqt
%{_includedir}/svnqt/*

%changelog
