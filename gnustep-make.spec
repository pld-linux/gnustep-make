Summary:	GNUstep Makefile package
Name:		gnustep-make
Version:	0.6.0
Release:	1
License:	GPL
Vendor:		The Seawood Project
Group:		Utilities/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Patch0:		gstep-make-nodupsh.patch
URL:		http://www.gnustep.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	gnustep-core

%description
This package contains the basic tools needed to run GNUstep
applications. Library combo is %{libcombo}. %{_buildblurb}

%package devel
Summary:	Files needed to develop applications with gnustep-make
Group:		Development/Tools
Group(fr):	Development/Outils
Group(pl):	Programowanie/Narzêdzia
Requires:	%{name} = %{version}

%description devel 
The makefile package is a simplistic, powerful and extensible way to
write makefiles for a GNUstep-based project. It allows the user to
write a GNUstep-based project without having to deal with the complex
issues associated with the configuration and installation of the core
GNUstep libraries. It also allows the user to easily create
cross-compiled binaries. Library combo is %{libcombo}. %{_buildblurb}

%prep
%setup -q -n gstep-%{version}/make
%patch -p2

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix}/GNUstep --with-library-combo=%{libcombo}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install GNUSTEP_INSTALLATION_DIR=${RPM_BUILD_ROOT}%{_prefix}/GNUstep

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
. %{_prefix}/GNUstep/Makefiles/GNUstep.sh
EOF

cat > mygnustep.csh << EOF
#!/bin/csh
source %{_prefix}/GNUstep/Makefiles/GNUstep.csh
EOF

chmod 755 mygnustep.*
mv mygnustep.sh $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh
mv mygnustep.csh $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh
%endif

cat > filelist.rpm.in << EOF
%defattr (-, bin, bin)
%doc COPYING DESIGN README
%ifos Linux
%config /etc/profile.d/GNUstep.csh
%config /etc/profile.d/GNUstep.sh
%endif

%dir %{_prefix}/GNUstep
%dir %{_prefix}/GNUstep/share
%dir %{_prefix}/GNUstep/Apps
%dir %{_prefix}/GNUstep/Makefiles
%dir %{_prefix}/GNUstep/Makefiles/GSARCH
%dir %{_prefix}/GNUstep/Makefiles/GSARCH/GSOS
%dir %{_prefix}/GNUstep/Library
%dir %{_prefix}/GNUstep/Library/info
%dir %{_prefix}/GNUstep/Library/PostScript
%dir %{_prefix}/GNUstep/Library/Services
%dir %{_prefix}/GNUstep/Library/man
%dir %{_prefix}/GNUstep/Tools

%{_prefix}/GNUstep/Makefiles/config*
%{_prefix}/GNUstep/Makefiles/*.csh
%{_prefix}/GNUstep/Makefiles/*.sh
%{_prefix}/GNUstep/Makefiles/GSARCH/GSOS/which_lib

%{_prefix}/GNUstep/Tools/debugapp
%{_prefix}/GNUstep/Tools/openapp
%{_prefix}/GNUstep/Tools/opentool

EOF

cat > filelist-devel.rpm.in << EOF
%defattr (-, bin, bin)
%config %{_prefix}/GNUstep/share/config.site
%config %{_prefix}/GNUstep/Makefiles/GSARCH/GSOS/config.make

%{_prefix}/GNUstep/Makefiles/*.func
%{_prefix}/GNUstep/Makefiles/*.make
%{_prefix}/GNUstep/Makefiles/*.template
%{_prefix}/GNUstep/Makefiles/install-sh
%{_prefix}/GNUstep/Makefiles/mkinstalldirs

EOF

sed -e "s|GSARCH|${tmp5}|" -e "s|GSOS|${tmp7}|" < filelist.rpm.in > filelist.rpm
sed -e "s|GSARCH|${tmp5}|" -e "s|GSOS|${tmp7}|" < filelist-devel.rpm.in > filelist-devel.rpm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f filelist.rpm
%defattr(644,root,root,755)

%files -f filelist-devel.rpm devel
%defattr(644,root,root,755)
