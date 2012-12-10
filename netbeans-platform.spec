Name:		libnb-platform7
Version:	6.0.1
Release:	7
%define section		devel
%define source_top	%{name}-src
%define netbeansdir     %{_datadir}/netbeans

%define clusterdir      %{netbeansdir}

Summary:	NetBeans Platform for Development of Rich Client Swing Applications
URL:		http://platform.netbeans.org
Source0:	http://core.netbeans.org/files/documents/12/1805/netbeans-platform-6.0.1-src.tar.gz
Source1: 	scripts.sh

Patch0:         10-build.patch
Patch1:         20-netbeans-autoupdate-backport-124809.patch

Epoch:		0
License:	GPLv2 with exceptions or CDDL
Group:		Development/Java
BuildArch:	noarch
BuildRequires:	java-devel >= 1.6.0
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	ant >= 0:1.6.3
BuildRequires:  ant-junit >= 1.6.3
BuildRequires:  ant-nodeps >= 0:1.6.3
BuildRequires:  ant-trax >= 0:1.6.3
BuildRequires:	junit >= 0:3.8.1
BuildRequires:	swing-layout >= 0:1.0
BuildRequires:  javahelp2 >= 2.0.05
Requires: 	java >= 0:1.6
Requires:	jpackage-utils >= 0:1.5
Requires:	swing-layout >= 0:1.0
Requires:	javahelp2 >= 2.0.05

%description
NetBeans Platform is a framework for development of 
rich client Swing applications. It contains powerful
module system and a set of modules providing various
functionalities needed for simplification of 
development of modular desktop applications.

%package javadoc
Summary: Javadoc documentation for NetBeans Platform
Group: Development/Java
%description javadoc
NetBeans Platform is a set of modules, each providing
their own APIs and working together or in a standalone
mode. This package provides one master 
javadoc to all of them.


%package devel
Summary: Build harness for NetBeans Platform
Group: Development/Java
Requires:   javahelp2 >= 2.0
%description devel
Harness with build scripts and ant tasks for everyone who
build an application on top of NetBeans Platform

%prep
%{__rm} -rf netbeans-src

%setup -q -c
find . -type d | xargs -t chmod 755
find . -type f -exec chmod 644 {} ";"
find . -type f \( -iname "*.jar" -o -iname "*.zip" \) | xargs -t %{__rm} -f

mv netbeans-platform-%{version}/* .

LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="%{buildroot}/%{_javadocdir}/netbeans-platform7"
RMF="%{__rm} -rf"
INS="cp -r"
NBDIR="%{buildroot}/%{clusterdir}"
JHJAR=javahelp2.jar
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR JHJAR
sh -x %{SOURCE1} setup 

%patch0 -p1 -b .sav
%patch1 -p1 -b .sav

%build

LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="%{buildroot}/%{_javadocdir}/netbeans-platform7"
RMF="%{__rm} -rf"
INS="cp -r"
NBDIR="%{buildroot}/%{clusterdir}"
JHJAR=javahelp2.jar
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR JHJAR

sh -x %{SOURCE1} build || exit 1
sh -x %{SOURCE1} build_devel || exit 1
sh -x %{SOURCE1} build_javadoc || exit 1


%install
LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="%{buildroot}/%{_javadocdir}/netbeans-platform7"
RMF="%{__rm} -rf"
INS="cp -r"
NBDIR="%{buildroot}/%{clusterdir}"
JHJAR=javahelp2.jar
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR JHJAR

%{__mkdir_p} $NBDIR

sh -x %{SOURCE1} install || exit 1
sh -x %{SOURCE1} install_devel || exit 1
sh -x %{SOURCE1} install_javadoc || exit 1


%files
%defattr(644,root,root,755)
%dir %{clusterdir}/platform7/
%{clusterdir}/platform7/*
# to prevent use of autoupdate on this directory
%{clusterdir}/platform7/.noautoupdate

%files devel
%defattr(644,root,root,755)
%dir %{clusterdir}/harness/
%{clusterdir}/harness/*
# to prevent use of autoupdate on this directory
%{clusterdir}/harness/.noautoupdate

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/netbeans-platform7




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:6.0.1-6mdv2011.0
+ Revision: 620165
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:6.0.1-5mdv2010.0
+ Revision: 429815
- rebuild

* Sat Jul 26 2008 Thierry Vignaud <tv@mandriva.org> 0:6.0.1-4mdv2009.0
+ Revision: 250295
- rebuild

* Fri Feb 29 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0.1-2mdv2008.1
+ Revision: 176871
+ rebuild (emptylog)

* Fri Feb 15 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0.1-1mdv2008.1
+ Revision: 168877
- Update to NetBeans 6.0.1 and change of the scripts structure to be more easily shareable with our ubuntu packages

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Wed Jan 16 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0-3mdv2008.1
+ Revision: 153646
- Alexander Kurtakov suggested to put NetBeans into /usr/share, as that will prevent unneeded differences between 32 and 64-bit architectures

* Tue Jan 15 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0-2mdv2008.1
+ Revision: 152616
- Backport of patch for issue #124809. Now autoupdate shall update platform without any exceptions

* Mon Jan 07 2008 Jaroslav Tulach <jtulach@mandriva.org> 0:6.0-1mdv2008.1
+ Revision: 146201
- Upgrading to final 6.0 version of NetBeans Platform

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:6.0-0rc1.2mdv2008.1
+ Revision: 120970
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Fri Nov 23 2007 Nicolas Vigier <nvigier@mandriva.com> 0:6.0-0rc1.1mdv2008.1
+ Revision: 111722
- add BuildRequires on java-devel >= 1.6.0
- fix release, netbeansdir, license, groups
- import libnb-platform7


* Fri Nov 16 2007 Jaroslav Tulach <jtulach z netbeans tecka org>
- Updating to RC1 of 6.0
* Sat Dec 2 2006 Jaroslav Tulach <jtulach z netbeans tecka org>
- Updating for M5 of 6.0
* Thu Mar 16 2006 Jaroslav Tulach <jtulach z netbeans tecka org>
- Adding the devel package
* Sat Mar 11 2006 Jaroslav Tulach <jtulach z netbeans tecka org>
- Turning the dependency on javahelp to conditional one
* Fri Feb 17 2006 Jaroslav Tulach <jtulach z netbeans tecka org> 
- Incorporating comments from David Walluck
* Fri Jan 27 2006 Jaroslav Tulach <jtulach z netbeans tecka org> 
- Initial version of the platform package

