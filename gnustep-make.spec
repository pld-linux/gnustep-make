# This package is not relocatable
%define ver	0.6.0
%define date	19990918
%define prefix 	/usr
%define gsr 	%{prefix}/GNUstep
%define libcombo gnu-gnu-gnu-xgps
Name: 		gnustep-make
Version: 	%{ver}
Release: 	1
Source: 	ftp://ftp.gnustep.org/pub/gnustep/core/gstep-make-%{ver}.tar.gz
Patch:          gstep-make-nodupsh.patch
Copyright: 	GPL
Group: 		System Environment/Base
Summary: 	GNUstep Makefile package
Packager:	Christopher Seawood <cls@seawood.org>
Distribution:	Seawood's Random RPMS (%{_buildsym})
Vendor:		The Seawood Project
URL:		http://www.gnustep.org/
BuildRoot: 	/var/tmp/build-%{name}
Conflicts:	gnustep-core

%description
This package contains the basic tools needed to run GNUstep applications.
Library combo is %{libcombo}.
%{_buildblurb}

%package devel
Summary: Files needed to develop applications with gnustep-make
Group: Development/Tools
Requires: %{name} = %{ver}

%description devel 
The makefile package is a simplistic, powerful and extensible way to
write makefiles for a GNUstep-based project.  It allows the user to
write a GNUstep-based project without having to deal with the complex
issues associated with the configuration and installation of the core
GNUstep libraries.  It also allows the user to easily create
cross-compiled binaries.
Library combo is %{libcombo}.
%{_buildblurb}

%prep
%setup -q -n gstep-%{ver}/make
%patch -p2 -b .nodupsh

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{gsr} --with-library-combo=%{libcombo}
make

%install
rm -rf $RPM_BUILD_ROOT
make install GNUSTEP_INSTALLATION_DIR=${RPM_BUILD_ROOT}%{gsr}

tmp1=`./config.guess`
tmp2=`./cpu.sh $tmp1`
tmp3=`./vendor.sh $tmp1`
tmp4=`./os.sh $tmp1`
tmp5=`./clean_cpu.sh $tmp2`
tmp6=`./clean_vendor.sh $tmp3`
tmp7=`./clean_os.sh $tmp4`

%ifos Linux
mkdir -p ${RPM_BUILD_ROOT}/etc/profile.d
# Create profile files
cat > mygnustep.sh << EOF
#!/bin/sh
. %{gsr}/Makefiles/GNUstep.sh
EOF

cat > mygnustep.csh << EOF
#!/bin/csh
source %{gsr}/Makefiles/GNUstep.csh
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

%dir %{gsr}
%dir %{gsr}/share
%dir %{gsr}/Apps
%dir %{gsr}/Makefiles
%dir %{gsr}/Makefiles/GSARCH
%dir %{gsr}/Makefiles/GSARCH/GSOS
%dir %{gsr}/Library
%dir %{gsr}/Library/info
%dir %{gsr}/Library/PostScript
%dir %{gsr}/Library/Services
%dir %{gsr}/Library/man
%dir %{gsr}/Tools

%{gsr}/Makefiles/config*
%{gsr}/Makefiles/*.csh
%{gsr}/Makefiles/*.sh
%{gsr}/Makefiles/GSARCH/GSOS/which_lib

%{gsr}/Tools/debugapp
%{gsr}/Tools/openapp
%{gsr}/Tools/opentool

EOF

cat > filelist-devel.rpm.in << EOF
%defattr (-, bin, bin)
%config %{gsr}/share/config.site
%config %{gsr}/Makefiles/GSARCH/GSOS/config.make

%{gsr}/Makefiles/*.func
%{gsr}/Makefiles/*.make
%{gsr}/Makefiles/*.template
%{gsr}/Makefiles/install-sh
%{gsr}/Makefiles/mkinstalldirs

EOF

sed -e "s|GSARCH|${tmp5}|" -e "s|GSOS|${tmp7}|" < filelist.rpm.in > filelist.rpm
sed -e "s|GSARCH|${tmp5}|" -e "s|GSOS|${tmp7}|" < filelist-devel.rpm.in > filelist-devel.rpm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f filelist.rpm
%files -f filelist-devel.rpm devel

%changelog
* Sat Sep 18 1999 Christopher Seawood <cls@seawood.org>
- Version 0.6.0
- Added nodupsh patch

* Sat Aug 07 1999 Christopher Seawood <cls@seawood.org>
- Updated to cvs dawn_6 branch

* Fri Jun 25 1999 Christopher Seawood <cls@seawood.org>
- Split into separate rpm from gnustep-core
- Build from cvs snapshot
- Added services patch
