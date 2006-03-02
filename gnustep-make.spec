#
# Conditional build:
%bcond_without	docs	# don't build documentation (for bootstrap)
#
Summary:	GNUstep Makefile package
Summary(pl):	Pakiet GNUstep Makefile
Name:		gnustep-make
Version:	1.11.2
Release:	2
License:	GPL
Vendor:		The GNUstep Project
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	87f563d71368ebb670c485ecdf198365
Patch0:		%{name}-destdir.patch
Patch1:		%{name}-no-LD_LIBRARY_PATH.patch
URL:		http://www.gnustep.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
%if %{with docs}
BuildRequires: gnustep-make-devel
# texi2html >= 1.61 (with -init_file) is included in tetex >= 3
BuildRequires:	tetex >= 1:3.0
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-format-plain
BuildRequires:	texinfo-texi2dvi
%endif
Requires:	gnustep-dirs
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/%{_lib}/GNUstep
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%(echo %{_target_cpu} | sed -e 's/amd64/x86_64/;s/ppc/powerpc/')
%endif

%description
This package contains the basic tools needed to run GNUstep
applications.

%description -l pl
Ten pakiet zawiera podstawowe narz�dzia potrzebne do uruchamiania
aplikacji GNUstep.

%package devel
Summary:	Files needed to develop applications with gnustep-make
Summary(pl):	Pliki potrzebne do tworzenia aplikacji przy u�yciu gnustep-make
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description devel
The makefile package is a simplistic, powerful and extensible way to
write makefiles for a GNUstep-based project. It allows the user to
write a GNUstep-based project without having to deal with the complex
issues associated with the configuration and installation of the core
GNUstep libraries. It also allows the user to easily create
cross-compiled binaries.

%description devel -l pl
Pakiet makefile jest prost�, wydajn� i rozszerzaln� metod� pisania
makefile'i do projekt�w opartych o GNUstep. Pozwala u�ytkownikowi na
tworzenie projekt�w z pomini�ciem skomplikowanych szczeg��w
konfiguracji i instalacji podstawowych bibliotek GNUstep. Pozwala
tak�e �atwo tworzy� kompilowane skro�nie binaria.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
%configure \
	--disable-flattened \
	--with-library-combo=gnu-gnu-gnu \
	--with-tar=tar

%{__make}

%if %{with docs}
%{__make} -C Documentation
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	special_prefix=$RPM_BUILD_ROOT

%if %{with docs}
%{__make} -C Documentation install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System
%endif

install -d $RPM_BUILD_ROOT/etc/profile.d
# Create profile files
cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh << EOF
#!/bin/sh
. %{_prefix}/System/Library/Makefiles/GNUstep.sh

if [ ! -d \$GNUSTEP_USER_ROOT ]; then
	mkdir \$GNUSTEP_USER_ROOT
	chmod +rwx \$GNUSTEP_USER_ROOT
fi
EOF

cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh << EOF
#!/bin/csh
source %{_prefix}/System/Library/Makefiles/GNUstep.csh

test -d \$GNUSTEP_USER_ROOT
if (\$status != 0) then
	mkdir \$GNUSTEP_USER_ROOT
	chmod +rwx \$GNUSTEP_USER_ROOT
endif
EOF

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation \
	-type f ! -name '*.html' ! -name '*.css' ! -name '*.gz' | xargs gzip -9nf

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
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/profile.d/GNUstep.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/profile.d/GNUstep.csh

%dir %{_sysconfdir}/GNUstep
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/GNUstep/GNUstep.conf

# GNUstep top-level
%dir %{_prefix}
%{_prefix}/Local
%dir %{_prefix}/System

# System domain
%{_prefix}/System/Applications
%dir %{_prefix}/System/Library
%{_prefix}/System/share
%attr(755,root,root) %{_prefix}/System/Tools

# System/Library folder
%{_prefix}/System/Library/ApplicationSupport
%{_prefix}/System/Library/Bundles
%{_prefix}/System/Library/ColorPickers
%{_prefix}/System/Library/Colors
%{_prefix}/System/Library/DocTemplates
%if %{with docs}
%docdir %{_prefix}/System/Library/Documentation
%dir %{_prefix}/System/Library/Documentation
%endif
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

%if %{with docs}
%dir %{_prefix}/System/Library/Documentation/Developer
%dir %{_prefix}/System/Library/Documentation/Developer/Make
%{_prefix}/System/Library/Documentation/Developer/Make/ReleaseNotes
%dir %{_prefix}/System/Library/Documentation/User
%{_prefix}/System/Library/Documentation/User/GNUstep
%dir %{_prefix}/System/Library/Documentation/info
%{_prefix}/System/Library/Documentation/info/*.info*
%dir %{_prefix}/System/Library/Documentation/man
%dir %{_prefix}/System/Library/Documentation/man/man1
%{_prefix}/System/Library/Documentation/man/man1/openapp.1*
%dir %{_prefix}/System/Library/Documentation/man/man7
%{_prefix}/System/Library/Documentation/man/man7/GNUstep.7*
%endif

%attr(755,root,root) %{_prefix}/System/Library/Makefiles/config.*
%{_prefix}/System/Library/Makefiles/tar-exclude-list
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/*.sh
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/*.csh
%dir %{_prefix}/System/Library/Makefiles/%{gscpu}
%dir %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/which_lib

%files devel
%defattr(644,root,root,755)
%if %{with docs}
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
