Summary:	GNUstep Makefile package
Summary(pl):	Pakiet GNUstep Makefile
Name:		gnustep-make
Version:	1.0.1
Release:	1
License:	GPL
Vendor:		The Seawood Project
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Patch0:		gstep-make-nodupsh.patch
Patch1:		gnustep.diff.make
URL:		http://www.gnustep.org/
BuildRequires:	texinfo-texi2dvi
BuildRequires:	tetex >= 1.0.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	gnustep-core

%description
This package contains the basic tools needed to run GNUstep
applications. Library combo is %{libcombo}. %{_buildblurb}

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
cross-compiled binaries. Library combo is %{libcombo}. %{_buildblurb}

%description devel -l pl
Pakiet makefile jest prost±, wydajn± i rozszerzaln± metod± pisania
makefile'i do projektów opartych o GNUstep. Pozwala u¿ytkownikowi na
tworzenie projektów z pominiêciem skomplikowanych szczegó³ów
konfiguracji i instalacji podstawowych bibliotek GNUstep. Pozwala
tak¿e ³atwo tworzyæ kroskompilowane binaria.

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
CFLAGS="%{rpmcflags}" ./configure --prefix=%{_prefix}/GNUstep \
	--host=%{_target_platform} --target=%{_target_platform}
# --with-library-combo=%{libcombo}
%{__make}

#cd  Documentation
make -C Documentation
#cd ..

%install
rm -rf $RPM_BUILD_ROOT
# {__make} install special_prefix=${RPM_BUILD_ROOT}
make install special_prefix=${RPM_BUILD_ROOT}

install Documentation/*.texi \
	${RPM_BUILD_ROOT}%{_prefix}/GNUstep/System/Documentation/info/

tmp1=`./config.guess`
tmp2=`./cpu.sh $tmp1`
tmp3=`./vendor.sh $tmp1`
tmp4=`./os.sh $tmp1`
tmp5=`./clean_cpu.sh $tmp2`
tmp6=`./clean_vendor.sh $tmp3`
tmp7=`./clean_os.sh $tmp4`

%ifos Linux
install -d ${RPM_BUILD_ROOT}/etc/profile.d
# Create profile files
cat > mygnustep.sh << EOF
#!/bin/sh
. %{_prefix}/GNUstep/System/Makefiles/GNUstep.sh
EOF

cat > mygnustep.csh << EOF
#!/bin/csh
source %{_prefix}/GNUstep/System/Makefiles/GNUstep.csh
EOF

chmod 755 mygnustep.*
mv -f mygnustep.sh $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh
mv -f mygnustep.csh $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh
%endif
      
cat > filelist.rpm.in << EOF
%defattr (-, bin, bin)
%doc COPYING ChangeLog FAQ NEWS README
%doc Documentation/DESIGN
%doc Documentation/*.html
%doc Documentation/*.ps
%doc Documentation/*.dvi
%ifos Linux
%config /etc/profile.d/GNUstep.csh
%config /etc/profile.d/GNUstep.sh
%endif

%dir %{_prefix}/GNUstep
%dir %{_prefix}/GNUstep/Local
%dir %{_prefix}/GNUstep/Local/Users
%dir %{_prefix}/GNUstep/Local/Users/Administrator
%dir %{_prefix}/GNUstep/Network
%dir %{_prefix}/GNUstep/System
%dir %{_prefix}/GNUstep/System/share
%dir %{_prefix}/GNUstep/System/Apps
%dir %{_prefix}/GNUstep/System/Documentation
%dir %{_prefix}/GNUstep/System/Documentation/info
%dir %{_prefix}/GNUstep/System/Documentation/man
%dir %{_prefix}/GNUstep/System/Library
%dir %{_prefix}/GNUstep/System/Library/Colors
%dir %{_prefix}/GNUstep/System/Library/PostScript
%dir %{_prefix}/GNUstep/System/Library/Services
%dir %{_prefix}/GNUstep/System/Makefiles
%dir %{_prefix}/GNUstep/System/Makefiles/Additional
%dir %{_prefix}/GNUstep/System/Makefiles/GSARCH
%dir %{_prefix}/GNUstep/System/Makefiles/GSARCH/GSOS
%dir %{_prefix}/GNUstep/System/Tools

%{_prefix}/GNUstep/System/Documentation/info/*.texi

%{_prefix}/GNUstep/System/Makefiles/config*
%{_prefix}/GNUstep/System/Makefiles/*.csh
%{_prefix}/GNUstep/System/Makefiles/*.sh
%{_prefix}/GNUstep/System/Makefiles/GSARCH/GSOS/which_lib

%{_prefix}/GNUstep/System/Tools/debugapp
%{_prefix}/GNUstep/System/Tools/openapp
%{_prefix}/GNUstep/System/Tools/opentool

EOF

cat > filelist-devel.rpm.in << EOF
%defattr (-, bin, bin)
%config %{_prefix}/GNUstep/System/share/config.site
%config %{_prefix}/GNUstep/System/Makefiles/GSARCH/GSOS/config.make

%{_prefix}/GNUstep/System/Makefiles/*.func
%{_prefix}/GNUstep/System/Makefiles/*.make
%{_prefix}/GNUstep/System/Makefiles/*.template
%{_prefix}/GNUstep/System/Makefiles/install-sh
%{_prefix}/GNUstep/System/Makefiles/mkinstalldirs

EOF

sed -e "s|GSARCH|${tmp5}|" -e "s|GSOS|${tmp7}|" < filelist.rpm.in > filelist.rpm
sed -e "s|GSARCH|${tmp5}|" -e "s|GSOS|${tmp7}|" < filelist-devel.rpm.in > filelist-devel.rpm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f filelist.rpm
%defattr(644,root,root,755)

%files -f filelist-devel.rpm devel
%defattr(644,root,root,755)
