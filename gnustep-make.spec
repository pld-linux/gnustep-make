Summary:	GNUstep Makefile package
Summary(pl):	Pakiet GNUstep Makefile
Name:		gnustep-make
Version:	1.5.1
Release:	0.1
License:	GPL
Vendor:		The Seawood Project
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Patch0:		gnustep-make-configure.patch
Patch1:		gnustep-make-doc.patch
URL:		http://www.gnustep.org/
BuildRequires:	tetex >= 1.0.7
BuildRequires:	texinfo-texi2dvi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	gnustep-core

%define         _prefix         /usr/lib/GNUstep

%description
This package contains the basic tools needed to run GNUstep
applications.

%description -l pl
Ten pakiet zawiera podstawowe narzêdzia potrzebne do uruchamiania
aplikacji GNUstep.

%package devel
Summary:	Files needed to develop applications with gnustep-make
Summary(pl):	Pliki potrzebne do tworzenia aplikacji przy u¿yciu gnustep-make
Group:		Development/Tools
Requires:	%{name} = %{version}

%description devel
The makefile package is a simplistic, powerful and extensible way to
write makefiles for a GNUstep-based project. It allows the user to
write a GNUstep-based project without having to deal with the complex
issues associated with the configuration and installation of the core
GNUstep libraries. It also allows the user to easily create
cross-compiled binaries.

%description devel -l pl
Pakiet makefile jest prost±, wydajn± i rozszerzaln± metod± pisania
makefile'i do projektów opartych o GNUstep. Pozwala u¿ytkownikowi na
tworzenie projektów z pominiêciem skomplikowanych szczegó³ów
konfiguracji i instalacji podstawowych bibliotek GNUstep. Pozwala
tak¿e ³atwo tworzyæ kroskompilowane binaria.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--prefix=%{_prefix} 
%{__make}
%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install special_prefix=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/System/Documentation/info
install Documentation/*.texi \
	$RPM_BUILD_ROOT%{_prefix}/System/Documentation/info

install -d $RPM_BUILD_ROOT/etc/profile.d
# Create profile files
cat > ./mygnustep.sh << EOF
#!/bin/sh
. %{_prefix}/System/Makefiles/GNUstep.sh
EOF

cat > mygnustep.csh << EOF
#!/bin/csh
source %{_prefix}/GNUstep/System/Makefiles/GNUstep.csh
EOF

chmod 755 mygnustep.*
mv -f mygnustep.sh $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh
mv -f mygnustep.csh $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ NEWS README
%doc Documentation/DESIGN
#%doc Documentation/*.info
%dir %{_prefix}
%{_prefix}/Local
%{_prefix}/Network
%dir %{_prefix}/System
%{_prefix}/System/Applications
%{_prefix}/System/Developer
%docdir %{_prefix}/System/Documentation
%{_prefix}/System/Documentation
%{_prefix}/System/Headers
%{_prefix}/System/Libraries
%{_prefix}/System/Library
%dir %{_prefix}/System/Makefiles
%attr(755,root,root) %{_prefix}/System/Makefiles/config.*
%attr(755,root,root) %{_prefix}/System/Makefiles/*.sh
%attr(755,root,root) %{_prefix}/System/Makefiles/*.csh
%dir %{_prefix}/System/Makefiles/ix86
%dir %{_prefix}/System/Makefiles/ix86/linux-gnu
%attr(755,root,root) %{_prefix}/System/Makefiles/ix86/linux-gnu/user_home
%attr(755,root,root) %{_prefix}/System/Makefiles/ix86/linux-gnu/which_lib
%{_prefix}/System/share
%attr(755,root,root) %{_prefix}/System/Tools

%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/profile.d/GNUstep.sh
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/profile.d/GNUstep.csh

%files devel
%defattr(644,root,root,755)
%{_prefix}/System/Makefiles/*.make
%{_prefix}/System/Makefiles/*.template
%{_prefix}/System/Makefiles/Instance
%{_prefix}/System/Makefiles/Master
%{_prefix}/System/Makefiles/ix86/linux-gnu/*.make
%attr(755,root,root) %{_prefix}/System/Makefiles/install-sh
%attr(755,root,root) %{_prefix}/System/Makefiles/mkinstalldirs
