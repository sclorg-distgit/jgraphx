%{?scl:%scl_package jgraphx}
%{!?scl:%global pkg_name %{name}}

%if 0%{?rhel}
# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}
%endif

Name:           %{?scl_prefix}jgraphx
Version:        3.1.2.0
Release:        60.2%{?dist}
Summary:        Java Graph Drawing Component

Group:          Development/Libraries
License:        BSD
URL:            http://www.jgraph.com/jgraph.html
Source0:        http://www.jgraph.com/downloads/jgraphx/archive/%{pkg_name}-%(echo %{version} |sed 's/\./_/g').zip
Source1:        bnd.properties

BuildRequires:  %{?scl_prefix_java_common}javapackages-local
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_maven}aqute-bnd
%{!?scl:
Requires:       java-headless
Requires:       jpackage-utils
}
%{?scl:Requires: %scl_runtime}

BuildArch:      noarch

%description
JGraphX is the a powerful, easy-to-use and feature-rich graph drawing
component for Java. It is a rewrite of JGraph, also known as JGraph 6.

%package javadoc
Summary:        API Documentation for %{name}
Group:          Documentation
%{!?scl:
Requires:       jpackage-utils
Requires:       %{name} = %{version}-%{release}
}
%{?scl:Requires: %scl_runtime}

%description javadoc
JavaDoc documentation for %{name}

%prep
%setup -q -n %{pkg_name}
find -name '*.jar' -delete
rm -rf docs/api

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
ant build maven-jar

#Convert to OSGi bundle
pushd lib
%if 0%{?fedora}
  bnd wrap --output %{pkg_name}.bar --properties %{SOURCE1} \
           --version %{version} %{pkg_name}.jar
%else
  java -jar $(build-classpath aqute-bnd) wrap -output jgraphx.bar -properties %{SOURCE1} %{pkg_name}.jar
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
* Wed Mar 30 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.1.2.0-60.2
- Own in-collection directory.
- Resolves: RHBZ#1317970

* Wed Jan 27 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.1.2.0-60.1
- Build for RHSCL 2.2.

* Thu Jul 23 2015 Severin Gehwolf <sgehwolf@redhat.com> - 3.1.2.0-5
- SCL-ize package.

* Fri Jul 17 2015 Severin Gehwolf <sgehwolf@redhat.com> - 3.1.2.0-4
- Wrap jar using aqute-bnd so as to provide OSGi metadata.
- Resolves: RHBZ#1240777

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Clément David <c.david86@gmail.com> - 3.1.2.0-2
- Provide maven pom.xml

* Tue Dec 09 2014 Clément David <c.david86@gmail.com> - 3.1.2.0-1
- Update version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Clément David <c.david86@gmail.com> - 2.5.0.2-1
- Update version

* Wed Oct 23 2013 Clément David <c.david86@gmail.com> - 2.1.0.7-2
- Remove versioned jars

* Fri Aug 02 2013 Clément David <c.david86@gmail.com> - 2.1.0.7-1
- Update version

* Fri Jul 26 2013 Clément David <c.david86@gmail.com> - 2.1.0.4-1
- Update version

* Tue Dec 04 2012 Clément David <c.david86@gmail.com> - 1.10.4.0-1
- Update version

* Thu Apr 05 2012 Clément David <c.david86@gmail.com> - 1.9.2.5-1
- Bump version

* Mon Apr 02 2012 Clément David <c.david86@gmail.com> - 1.9.2.4-2
- Update version

* Wed Sep 29 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.4.1.0-2
- Drop files in %%prep, fix URL (Markus Mayer)

* Mon Sep 20 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.4.1.0-1
- Bump version
- Fix URL (Markus Mayer)
- Add required dependencies (Markus Mayer)

* Thu Apr 29 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.3.1.6-1
- Initial packaging
