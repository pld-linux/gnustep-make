#
Summary:	GNUstep Makefile package
Summary(pl.UTF-8):	Pakiet GNUstep Makefile
Name:		gnustep-make
Version:	2.0.7
Release:	1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	1a4b3cf7cca6d1e90b84034012480630
Source1:	%{name}-fslayout-pld
Patch0:		%{name}-no-LD_LIBRARY_PATH.patch
Patch1:		%{name}-no-chain-library-links.patch
URL:		http://www.gnustep.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
# texi2html >= 1.61 (with -init_file) is included in tetex >= 3
BuildRequires:	tetex >= 1:3.0
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-format-plain
BuildRequires:	texinfo-texi2dvi
Requires:	gnustep-dirs
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the basic tools needed to run GNUstep
applications.

%description -l pl.UTF-8
Ten pakiet zawiera podstawowe narzędzia potrzebne do uruchamiania
aplikacji GNUstep.

%package devel
Summary:	Files needed to develop applications with gnustep-make
Summary(pl.UTF-8):	Pliki potrzebne do tworzenia aplikacji przy użyciu gnustep-make
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description devel
The makefile package is a simplistic, powerful and extensible way to
write makefiles for a GNUstep-based project. It allows the user to
write a GNUstep-based project without having to deal with the complex
issues associated with the configuration and installation of the core
GNUstep libraries. It also allows the user to easily create
cross-compiled binaries.

%description devel -l pl.UTF-8
Pakiet makefile jest prostą, wydajną i rozszerzalną metodą pisania
makefile'i do projektów opartych o GNUstep. Pozwala użytkownikowi na
tworzenie projektów z pominięciem skomplikowanych szczegółów
konfiguracji i instalacji podstawowych bibliotek GNUstep. Pozwala
także łatwo tworzyć kompilowane skrośnie binaria.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
cp %{SOURCE1} FilesystemLayouts/pld

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
%configure \
	--with-library-combo=gnu-gnu-gnu \
	--with-layout=pld \
	--with-tar=tar

%{__make}

#GNUSTEP_MAKEFILES=`pwd` %{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	special_prefix=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/profile.d
# Create profile files
cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh << EOF
#!/bin/sh
. %{_datadir}/GNUstep/Makefiles/GNUstep.sh

if [ ! -d \$GNUSTEP_USER_ROOT ]; then
	mkdir \$GNUSTEP_USER_ROOT
	chmod +rwx \$GNUSTEP_USER_ROOT
fi
EOF

cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh << EOF
#!/bin/csh
source %{_datadir}Makefiles/GNUstep.csh

test -d \$GNUSTEP_USER_ROOT
if (\$status != 0) then
	mkdir \$GNUSTEP_USER_ROOT
	chmod +rwx \$GNUSTEP_USER_ROOT
endif
EOF

# Remove excessive escaping and fix lib/lib64 dir
sed -i -e 's|"/usr"|/usr|g' -e 's|/lib|/%{_lib}|g' $RPM_BUILD_ROOT/etc/GNUstep/GNUstep.conf

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
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/debugapp.1*
%{_mandir}/man1/gnustep-config.1*
%{_mandir}/man1/openapp.1*
%{_mandir}/man1/opentool.1*
%{_mandir}/man7/GNUstep.7*
%{_mandir}/man7/library-combo.7*


%dir %{_sysconfdir}/GNUstep
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/GNUstep/GNUstep.conf

# GNUstep top-level
%dir %{_datadir}/GNUstep

# System/Library folder
%dir %{_datadir}/GNUstep/Makefiles

%if %{with doc}
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

%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/config.*
%{_datadir}/GNUstep/Makefiles/tar-exclude-list
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/*.sh
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/*.csh

%files devel
%defattr(644,root,root,755)
%if %{with doc}
%docdir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Documentation/Developer/Make/Manual
%endif

%{_datadir}/GNUstep/Makefiles/*.make
%{_datadir}/GNUstep/Makefiles/*.template
%{_datadir}/GNUstep/Makefiles/Instance
%{_datadir}/GNUstep/Makefiles/Master
%{_datadir}/GNUstep/Makefiles/gnustep-make-help

%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/install-sh
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/mkinstalldirs
