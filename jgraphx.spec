%{?scl:%scl_package jgraphx}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

%if 0%{?rhel}

%if 0%{?rhel} <= 6
  # EL 6
  %global custom_release 60
%else
  # EL 7
  %global custom_release 70
%endif

%else

%global custom_release 1

%endif

Name:           %{?scl_prefix}jgraphx
Version:        3.1.2.0
Release:        %{custom_release}.3%{?dist}
Summary:        Java Graph Drawing Component

Group:          Development/Libraries
License:        BSD
URL:            http://www.jgraph.com/jgraph.html
Source0:        http://www.jgraph.com/downloads/jgraphx/archive/%{pkg_name}-%(echo %{version} |sed 's/\./_/g').zip
Source1:        bnd.properties

BuildRequires:  %{?scl_prefix_maven}javapackages-local
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_maven}aqute-bnd

BuildArch:      noarch

%description
JGraphX is the a powerful, easy-to-use and feature-rich graph drawing
component for Java. It is a rewrite of JGraph, also known as JGraph 6.

%package javadoc
Summary:        API Documentation for %{name}
Group:          Documentation

%description javadoc
JavaDoc documentation for %{name}

%prep
%setup -q -n %{pkg_name}
find -name '*.jar' -delete
rm -rf docs/api

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -x
ant build maven-jar

#Convert to OSGi bundle
pushd lib
# Make versions 3 parts only. That is: A.B.C.D => A.B.C
VER=$(echo %{version} | sed 's/^\([0-9]\+\.[0-9]\+\.[0-9]\+\)\.[0-9]\+$/\1/')
sed "s/__VERSION__/$VER/g" %{SOURCE1} > bnd.props
%if 0%{?fedora}
  bnd wrap --output %{pkg_name}.bar --properties bnd.props \
           --version $VER %{pkg_name}.jar
%else
  java -jar $(build-classpath aqute-bnd) wrap -output jgraphx.bar -properties bnd.props %{pkg_name}.jar
%endif
mv %{pkg_name}.bar %{pkg_name}.jar
popd
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_artifact pom.xml lib/%{pkg_name}.jar
%mvn_install -J docs/api/
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%if 0%{?rhel} <= 6
  %doc license.txt
%else
  %license license.txt
%endif

%files javadoc -f .mfiles-javadoc
%if 0%{?rhel} <= 6
  %doc license.txt
%else
  %license license.txt
%endif

%changelog
* Tue Jan 17 2017 Jie Kang <jkang@redhat.com> - 3.1.2.0-3
- Rebuild for RHSCL 2.4.

* Mon Jun 27 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.1.2.0-2
- Be sure to use 3 parts in BSN only.

* Fri Jun 24 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.1.2.0-1
- Initial package.
