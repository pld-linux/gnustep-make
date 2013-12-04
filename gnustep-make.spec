#
# Conditional build:
%bcond_with	bootstrap	# don't use existing installation for docs build
%bcond_without	doc		# documentation build
#
Summary:	GNUstep Makefile package
Summary(pl.UTF-8):	Pakiet GNUstep Makefile
Name:		gnustep-make
Version:	2.6.5
Release:	3
License:	GPL v3+
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	1e143d2c920cef02535ab533af8b1846
Source1:	%{name}-fslayout-pld
Patch0:		%{name}-no-chain-library-links.patch
URL:		http://www.gnustep.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
%if %{with doc}
%{!?with_bootstrap:BuildRequires:	gnustep-make-devel >= 2}
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
cp %{SOURCE1} FilesystemLayouts/pld
%if "%{_lib}" != "lib"
%{__sed} -i -e 's,/lib\>,/%{_lib},g' FilesystemLayouts/pld
%endif

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
%configure \
	--with-library-combo=gnu-gnu-gnu \
	--with-layout=pld \
	--with-tar=tar

%{__make}

%if %{with doc}
%{?with_bootstrap:unset GNUSTEP_MAKEFILES}
%{__make} -C Documentation \
	%{!?with_bootstrap:GNUSTEP_MAKEFILES=%{_datadir}/GNUstep/Makefiles}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} -C Documentation install \
	DESTDIR=$RPM_BUILD_ROOT \
	GNUSTEP_MAKEFILES=$RPM_BUILD_ROOT%{_datadir}/GNUstep/Makefiles

%{__rm} $RPM_BUILD_ROOT%{_datadir}/GNUstep/Documentation/User/GNUstep/README.{Cygwin,Darwin,MinGW*}

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_datadir}/GNUstep/Documentation \
	-type f ! -name '*.html' ! -name '*.css' ! -name '*.pdf' ! -name '*.ps' | xargs gzip -9nf

%else
# just Documentation tree for other gnustep-* packages
install -d $RPM_BUILD_ROOT%{_datadir}/GNUstep/Documentation/{Developer,User/GNUstep}
%endif

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
source %{_datadir}/Makefiles/GNUstep.csh

test -d \$GNUSTEP_USER_ROOT
if (\$status != 0) then
	mkdir \$GNUSTEP_USER_ROOT
	chmod +rwx \$GNUSTEP_USER_ROOT
endif
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# here only files not packaged by make -C Documentation install
%doc ChangeLog* FAQ GNUstep-HOWTO
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/profile.d/GNUstep.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/profile.d/GNUstep.csh
%attr(755,root,root) %{_bindir}/debugapp
%attr(755,root,root) %{_bindir}/gnustep-config
%attr(755,root,root) %{_bindir}/gnustep-tests
%attr(755,root,root) %{_bindir}/openapp
%attr(755,root,root) %{_bindir}/opentool
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

%docdir %{_datadir}/GNUstep/Documentation
%dir %{_datadir}/GNUstep/Documentation
%dir %{_datadir}/GNUstep/Documentation/Developer
%dir %{_datadir}/GNUstep/Documentation/User
%dir %{_datadir}/GNUstep/Documentation/User/GNUstep
%if %{with doc}
%dir %{_datadir}/GNUstep/Documentation/Developer/Make
%{_datadir}/GNUstep/Documentation/Developer/Make/ReleaseNotes
%{_datadir}/GNUstep/Documentation/User/GNUstep/gnustep-faq.pdf
%{_datadir}/GNUstep/Documentation/User/GNUstep/gnustep-filesystem.pdf
%{_datadir}/GNUstep/Documentation/User/GNUstep/gnustep-howto.pdf
%{_datadir}/GNUstep/Documentation/User/GNUstep/gnustep-userfaq.pdf

%{_infodir}/gnustep-faq.info*
%{_infodir}/gnustep-howto.info*
%{_infodir}/gnustep-make.info*
%{_infodir}/gnustep-userfaq.info*
%endif

%dir %{_datadir}/GNUstep/Makefiles

%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/config.guess
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/config.sub
%{_datadir}/GNUstep/Makefiles/tar-exclude-list
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/*.sh
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/*.csh

%files devel
%defattr(644,root,root,755)
%if %{with doc}
%docdir %{_datadir}/GNUstep/Documentation
%{_datadir}/GNUstep/Documentation/Developer/Make/Manual
%endif

%{_datadir}/GNUstep/Makefiles/*.make
%{_datadir}/GNUstep/Makefiles/*.template
%{_datadir}/GNUstep/Makefiles/Instance
%{_datadir}/GNUstep/Makefiles/Master
%{_datadir}/GNUstep/Makefiles/gnustep-make-help

%dir %{_datadir}/GNUstep/Makefiles/TestFramework
%{_datadir}/GNUstep/Makefiles/TestFramework/GNUmakefile.in
%{_datadir}/GNUstep/Makefiles/TestFramework/*Testing.h
%{_datadir}/GNUstep/Makefiles/TestFramework/README
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/TestFramework/Summary.sh
%{_datadir}/GNUstep/Makefiles/TestFramework/example*.m

%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/install-sh
%attr(755,root,root) %{_datadir}/GNUstep/Makefiles/mkinstalldirs
