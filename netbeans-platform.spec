Name:		libnb-platform7
Version:	6.0
Release:	%mkrel 1
%define section		devel
%define source_top	%{name}-src
%define netbeansdir     %{_prefix}/lib/netbeans

%define clusterdir      %{netbeansdir}

Summary:	NetBeans Platform for Development of Rich Client Swing Applications
URL:		http://platform.netbeans.org
Source0:	http://download.netbeans.org/netbeans/6.0/final/zip/netbeans-6.0-200711261600-platform-src.zip

Patch0:         netbeans-platform-build.patch

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

%{__ln_s} %{_javadir}/javahelp2.jar core/javahelp/external/jh-2.0_05.jar
%{__ln_s} %{_javadir}/javahelp2.jar apisupport/harness/external/jsearch-2.0_05.jar
%{__ln_s} %{_javadir}/swing-layout.jar libs/swing-layout/external/swing-layout-1.0.3.jar

# generate empty javax.script file, so there is something in jsr223 API module
%{__mkdir_p} libs/jsr223/src/javax/script/
echo "package javax.script; class empty { }" > libs/jsr223/src/javax/script/empty.java

%{__mkdir_p} libs/jsr223/external
jar cf libs/jsr223/external/jsr223-api.jar libs/jsr223/src/javax/script/empty.java

%patch0 -b .sav

%build
(cd nbbuild 
ant \
  -Djpp.repo=%{_javadir} \
  -Dexternal.dir=%{_javadir} \
  -Dant.jar=$(find-jar ant) \
  -Dfile.reference.ant.jar=$(find-jar ant) \
  -Dbuild.compiler.deprecation=false \
  -Dbuild.compiler.debug=false \
  -Dverify.checkout=false \
  -Dpermit.jdk6.builds=true \
  build-platform
) || exit 1

(cd apisupport/harness
ant \
  -Djpp.repo=%{_javadir} \
  -Dexternal.dir=%{_javadir} \
  -Dant.jar=$(find-jar ant) \
  -Dfile.reference.ant.jar=$(find-jar ant) \
  -Dbuild.compiler.deprecation=false \
  -Dbuild.compiler.debug=false \
  -Dverify.checkout=false \
  -Dpermit.jdk6.builds=true \
) || exit 1

#(cd libs/external
#ant
#)

(cd nbbuild
ant \
  -Djpp.repo=%{_javadir} \
  -Dexternal.dir=%{_javadir} \
  -Dant.jar=$(find-jar ant) \
  -Dfile.reference.ant.jar=$(find-jar ant) \
  -Dbuild.compiler.deprecation=false \
  -Dbuild.compiler.debug=false \
  -Dverify.checkout=false \
  -Dpermit.jdk6.builds=true \
  -Dallmodules=\
  -Dcluster.config=platform,\
  -Dconfig.javadoc.cluster=platform7\
  -Dconfig.javadoc.netbeans=openide/util,openide/actions,openide/options,openide/awt,\
openide/dialogs,openide/nodes,openide/explorer,openide/fs,openide/modules,\
openide/text,openide/windows,openide/loaders,openide/io,projects/queries,\
core/progress,core/settings,core/javahelp,openide/execution,\
core/sendopts,core/options,editor/mimelookup\
  -Djavadoc.docs.org-netbeans-api-java=http://www.netbeans.org/download/6_0/javadoc/org-netbeans-api-java/\
  -Djavadoc.docs.org-netbeans-modules-project-ant=http://www.netbeans.org/download/6_0/javadoc/org-netbeans-modules-project-ant/\
  -Djavadoc.docs.org-netbeans-modules-projectapi=http://www.netbeans.org/download/6_0/javadoc/org-netbeans-modules-projectapi/\
  build-javadoc 
) || exit 1

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir_p} ${RPM_BUILD_ROOT}%{_bindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}
%{__mkdir_p} ${RPM_BUILD_ROOT}/%{clusterdir}

# build initial path structure
pushd nbbuild/netbeans
    %{__cp} -r platform7 ${RPM_BUILD_ROOT}/%{clusterdir}
    %{__chmod} a+x ${RPM_BUILD_ROOT}/%{clusterdir}/platform7/lib/nbexec
popd
# remove launchers for other os
%{__rm} -f ${RPM_BUILD_ROOT}/%{clusterdir}/platform7/lib/nbexec.exe
%{__rm} -f ${RPM_BUILD_ROOT}/%{clusterdir}/platform7/lib/nbexec.cmd
# make this cluster disabled for autoupdate
echo >${RPM_BUILD_ROOT}/%{clusterdir}/platform7/.noautoupdate

# link shared libraries to places NetBeans expect them at
%{__rm} $RPM_BUILD_ROOT/%{clusterdir}/platform7/modules/ext/swing-layout-1.0.3.jar
%{__ln_s} %{_javadir}/swing-layout.jar $RPM_BUILD_ROOT/%{clusterdir}/platform7/modules/ext/swing-layout-1.0.3.jar
# the link to javahelp2 can be broken is javahelp2 package is not installed:
#   - should not matter
#   - the platform does not need it by itself
#   - it just contains a wrapper
#   - every package that is using netbeans platform and requires javahelp2 to work should add a dep on javahelp2
#
%{__rm} $RPM_BUILD_ROOT/%{clusterdir}/platform7/modules/ext/jh-2.0_05.jar
%{__ln_s} %{_javadir}/javahelp2.jar $RPM_BUILD_ROOT/%{clusterdir}/platform7/modules/ext/jh-2.0_05.jar

# now copy the javadoc
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadocdir}/netbeans-platform7
%{__cp} -pr nbbuild/build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/netbeans-platform7
%{__rm} $RPM_BUILD_ROOT%{_javadocdir}/netbeans-platform7/*.zip


# copy the harness
pushd nbbuild/netbeans
    %{__cp} -r harness ${RPM_BUILD_ROOT}/%{clusterdir}
    # replace it with link to javahelp2
    %{__rm} $RPM_BUILD_ROOT/%{clusterdir}/harness/jsearch-2.0_05.jar
    %{__ln_s} %{_javadir}/javahelp2.jar $RPM_BUILD_ROOT/%{clusterdir}/harness/jsearch-2.0_05.jar
popd
# make this cluster disabled for autoupdate
echo >${RPM_BUILD_ROOT}/%{clusterdir}/harness/.noautoupdate

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
# to prevent use of autoupdate on this directory
%{clusterdir}/harness/.noautoupdate

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/netbeans-platform7


