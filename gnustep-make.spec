#
# Conditional build:
# _without_doc	- don't generate documentation (bootstrap build w/o gnustep-base)
#
Summary:	GNUstep Makefile package
Summary(pl):	Pakiet GNUstep Makefile
Name:		gnustep-make
Version:	1.7.1
Release:	1
License:	GPL
Vendor:		The GNUstep Project
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	5b349dd804785f335392ef4749e72a6d
URL:		http://www.gnustep.org/
BuildRequires:	autoconf
%{!?_without_doc:BuildRequires:	tetex >= 1.0.7}
%{!?_without_doc:BuildRequires:	texinfo-texi2dvi}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	gnustep-core

%define         _prefix         /usr/lib/GNUstep
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%{_target_cpu}
%endif

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

%build
%{__autoconf}
%configure

%{__make}

%if %{?_without_doc:0}%{!?_without_doc:1}
%{__make} -C Documentation
%endif


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	special_prefix=$RPM_BUILD_ROOT

%if %{?_without_doc:0}%{!?_without_doc:1}
%{__make} -C Documentation install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System
%endif

install -d $RPM_BUILD_ROOT/etc/profile.d
# Create profile files
cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh << EOF
#!/bin/sh
. %{_prefix}/System/Library/Makefiles/GNUstep.sh
EOF

cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh << EOF
#!/bin/csh
source %{_prefix}/GNUstep/System/Library/Makefiles/GNUstep.csh
EOF

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation \
	-type f ! -name '*.html' ! -name '*.css' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -d %{_prefix}/System/Makefiles -a ! -L %{_prefix}/System/Makefiles ]; then
	[ -d %{_prefix}/System/Library ] || install -d %{_prefix}/System/Library
	mv -f %{_prefix}/System/Makefiles %{_prefix}/System/Library
	ln -sf Library/Makefiles %{_prefix}/System/Makefiles
	echo 'Reinstall gnustep-make and gnustep-make-devel if some files are missing.' >&2
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/profile.d/GNUstep.sh
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/profile.d/GNUstep.csh

# GNUstep top-level
%dir %{_prefix}
%{_prefix}/Local
%{_prefix}/Network
%dir %{_prefix}/System

# System domain
%{_prefix}/System/Applications
%dir %{_prefix}/System/Library
# compatibility symlink
%{_prefix}/System/Makefiles
%{_prefix}/System/share
%attr(755,root,root) %{_prefix}/System/Tools

# System/Library folder
%{_prefix}/System/Library/ApplicationSupport
%{_prefix}/System/Library/Bundles
%{_prefix}/System/Library/ColorPickers
%{_prefix}/System/Library/Colors
%{_prefix}/System/Library/DocTemplates
%docdir %{_prefix}/System/Library/Documentation
%dir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Fonts
%{_prefix}/System/Library/Frameworks
%{_prefix}/System/Library/Headers
%{_prefix}/System/Library/Images
%{_prefix}/System/Library/KeyBindings
%{_prefix}/System/Library/Libraries
%dir %{_prefix}/System/Library/Makefiles
%{_prefix}/System/Library/PostScript
%{_prefix}/System/Library/Services
%{_prefix}/System/Library/Sounds

%if 0%{!?_without_doc:1}
%dir %{_prefix}/System/Library/Documentation/Developer
%dir %{_prefix}/System/Library/Documentation/Developer/Make
%{_prefix}/System/Library/Documentation/Developer/Make/ReleaseNotes
%dir %{_prefix}/System/Library/Documentation/User
%{_prefix}/System/Library/Documentation/User/GNUstep
%dir %{_prefix}/System/Library/Documentation/info
%{_prefix}/System/Library/Documentation/info/*.info*
%dir %{_prefix}/System/Library/Documentation/man
%endif

%attr(755,root,root) %{_prefix}/System/Library/Makefiles/config.*
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/*.sh
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/*.csh
%dir %{_prefix}/System/Library/Makefiles/%{gscpu}
%dir %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/user_home
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/which_lib

%files devel
%defattr(644,root,root,755)
%if 0%{!?_without_doc:1}
%docdir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Documentation/Developer/Make/Manual
%endif

%{_prefix}/System/Library/Makefiles/*.make
%{_prefix}/System/Library/Makefiles/*.template
%{_prefix}/System/Library/Makefiles/Instance
%{_prefix}/System/Library/Makefiles/Master
%{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/*.make
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/install-sh
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/mkinstalldirs
