#!/bin/sh

set -x

[ -z "$MKDIRP" ] && exit 1
[ -z "$RMF" ] && exit 1
[ -z "$LNS" ] && exit 1
[ -z "$INS" ] && exit 1
[ -z "$JAVADIR" ] && exit 1
[ -z "$JAVADOCDIR" ] && exit 1
[ -z "$NBDIR" ] && exit 1
[ -z "$JHJAR" ] && exit 1

setup() {
	# generate empty javax.script file, so there is something in jsr223 API module
	$MKDIRP libs/jsr223/src/javax/script
	echo "package javax.script; class empty { }" > libs/jsr223/src/javax/script/empty.java
	$MKDIRP libs/jsr223/external
	jar cf libs/jsr223/external/jsr223-api.jar libs/jsr223/src/javax/script/empty.java
	$LNS $JAVADIR/swing-layout.jar libs/swing-layout/external/swing-layout-1.0.3.jar
	$LNS $JAVADIR/$JHJAR apisupport/harness/external/jsearch-2.0_05.jar
	$LNS $JAVADIR/$JHJAR core/javahelp/external/jh-2.0_05.jar
}
	
build() {
	ant \
	-Dpermit.jdk6.builds=true \
	-Dbuild.compiler.deprecation=false \
	-Dbuild.compiler.debug=false \
	-Dverify.checkout=false \
	-f nbbuild/build.xml build-platform
}        
        

install() {
	$RMF nbbuild/netbeans/platform7/modules/ext/swing-layout-1.0.3.jar
	$RMF nbbuild/netbeans/platform7/modules/ext/jsearch-2.0_05.jar
	$RMF nbbuild/netbeans/platform7/modules/ext/jh-2.0_05.jar
	echo > nbbuild/netbeans/platform7/.noautoupdate
        $MKDIRP $NBDIR/platform7
	$INS nbbuild/netbeans/platform7/* ${NBDIR}/platform7
	$INS nbbuild/netbeans/platform7/.noautoupdate ${NBDIR}/platform7
	$LNS ${JAVADIR}/swing-layout.jar ${NBDIR}/platform7/modules/ext/swing-layout-1.0.3.jar
	$LNS ${JAVADIR}/$JHJAR ${NBDIR}/platform7/modules/ext/jh-2.0_05.jar
}


build_devel() {
	ant \
	-Dpermit.jdk6.builds=true \
	-Dbuild.compiler.deprecation=false \
	-Dbuild.compiler.debug=false \
	-Dverify.checkout=false \
	-f apisupport/harness/build.xml
}


install_devel() {
	$RMF nbbuild/netbeans/harness/jsearch-2.0_05.jar
	echo > nbbuild/netbeans/harness/.noautoupdate
        $MKDIRP $NBDIR/harness
	$INS nbbuild/netbeans/harness/* $NBDIR/harness
	$INS nbbuild/netbeans/harness/.noautoupdate $NBDIR/harness
	$LNS $JAVADIR/$JHJAR $NBDIR/harness/jsearch-2.0_05.jar
}

build_javadoc() {	
	ant \
	-Dpermit.jdk6.builds=true \
	-Dbuild.compiler.deprecation=false \
	-Dbuild.compiler.debug=false \
	-Dverify.checkout=false \
	-Dallmodules= \
	-Dcluster.config=platform \
	-Dconfig.javadoc.cluster=platform7 \
	-Dconfig.javadoc.netbeans=\
openide/util,openide/actions,openide/options,openide/awt,\
openide/dialogs,openide/nodes,openide/explorer,openide/fs,openide/modules,\
openide/text,openide/windows,openide/loaders,openide/io,projects/queries,\
core/progress,core/settings,core/javahelp,openide/execution,\
core/sendopts,core/options,editor/mimelookup \
	-Djavadoc.docs.org-netbeans-api-java=http://www.netbeans.org/download/6_0/javadoc/org-netbeans-api-java/ \
	-Djavadoc.docs.org-netbeans-modules-project-ant=http://www.netbeans.org/download/6_0/javadoc/org-netbeans-modules-project-ant/ \
	-Djavadoc.docs.org-netbeans-modules-projectapi=http://www.netbeans.org/download/6_0/javadoc/org-netbeans-modules-projectapi/ \
	-f nbbuild/build.xml build-javadoc
}

install_javadoc() {
	# copy core platform files
	$RMF nbbuild/build/javadoc/*.zip
        $MKDIRP $JAVADOCDIR
	$INS nbbuild/build/javadoc/* $JAVADOCDIR
}




case $1 in
setup)
	setup 
        ;;
build)
	build
        ;;
build_devel)
	build_devel
        ;;
build_javadoc)
	build_javadoc
        ;;
install)
	install
        ;;
install_devel)
	install_devel
        ;;
install_javadoc)
	install_javadoc
        ;;
*)
	exit 1
        ;;
esac

