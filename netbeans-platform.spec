Name:		libnb-platform7
Version:	6.0.1
Release:	%mkrel 1
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
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
JAVADOCDIR="%{_javadocdir}"
RMF="%{__rm_f}"
INS="%{__install}"
NBDIR="$RPM_BUILD_ROOT/%{clusterdir}"
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR
sh -x %{SOURCE1} setup 

%patch0 -p1 -b .sav
%patch1 -p1 -b .sav

%build

LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="%{_javadocdir}"
RMF="%{__rm_f}"
INS="%{__install}"
NBDIR="$RPM_BUILD_ROOT/%{clusterdir}"
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR

sh -x %{SOURCE1} build || exit 1
sh -x %{SOURCE1} build_devel || exit 1
sh -x %{SOURCE1} build_javadoc || exit 1


%install

%{__rm} -rf $RPM_BUILD_ROOT
LNS="%{__ln_s}"
MKDIRP="%{__mkdir_p}"
JAVADIR="%{_javadir}"
JAVADOCDIR="%{_javadocdir}"
RMF="%{__rm_f}"
INS="%{__install}"
NBDIR="$RPM_BUILD_ROOT/%{clusterdir}"
export LNS MKDIRP JAVADIR JAVADOCDIR RMF INS NBDIR

sh -x %{SOURCE1} install || exit 1
sh -x %{SOURCE1} install_devel || exit 1
sh -x %{SOURCE1} install_javadoc || exit 1


%clean
%{__rm} -rf $RPM_BUILD_ROOT

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
%{clusterdir}/harness/jsearch-2.0_05.jar
# to prevent use of autoupdate on this directory
%{clusterdir}/harness/.noautoupdate

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/netbeans-platform7


