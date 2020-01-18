%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global module pyasn1
%global modules_version 0.0.8

Name:           python-pyasn1
Version:        0.1.9
Release:        7%{?dist}
Summary:        ASN.1 tools for Python
License:        BSD
Group:          System Environment/Libraries
Source0:        http://downloads.sourceforge.net/pyasn1/pyasn1-%{version}.tar.gz
Source1:        http://downloads.sourceforge.net/pyasn1/pyasn1-modules-%{modules_version}.tar.gz
URL:            http://pyasn1.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
This is an implementation of ASN.1 types and codecs in the Python programming
language.

%package -n python2-pyasn1
Summary:    ASN.1 tools for Python 2
%{?python_provide:%python_provide python2-pyasn1}
%{!?python_provide:Provides: python-pyasn1 = %{version}-%{release}}
Obsoletes: python-pyasn1 < 0.1.9-3

%description -n python2-pyasn1
This is an implementation of ASN.1 types and codecs in the Python 2 programming
language.

%package -n python2-pyasn1-modules
Summary:    Modules for pyasn1
Requires:   python-pyasn1 >= %{version}-%{release}
%{?python_provide:%python_provide python2-pyasn1-modules}
%{!?python_provide:Provides: python-pyasn1-modules = %{version}-%{release}}
Obsoletes: python-pyasn1-modules < 0.1.9-3

%description -n python2-pyasn1-modules
ASN.1 types modules for python-pyasn1.

%package -n python3-pyasn1
Summary:    ASN.1 tools for Python 3
%{?python_provide:%python_provide python3-pyasn1}

%description -n python3-pyasn1
This is an implementation of ASN.1 types and codecs in the Python 3 programming
language.

%package -n python3-pyasn1-modules
Summary:    Modules for pyasn1
Requires:   python3-pyasn1 >= %{version}-%{release}
%{?python_provide:%python_provide python3-modules}

%description -n python3-pyasn1-modules
ASN.1 types modules for python3-pyasn1.


%prep
%setup -n %{module}-%{version} -q -b1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
cp -a ../pyasn1-modules-%{modules_version} %{py3dir}-modules
%endif


%build
%{__python} setup.py build
pushd ../pyasn1-modules-%{modules_version}
%{__python} setup.py build
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
pushd %{py3dir}-modules
%{__python3} setup.py build
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
pushd %{py3dir}-modules
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
pushd ../pyasn1-modules-%{modules_version}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd


%check
# PYTHONPATH is required because the the tests expect python{,3}-pyasn1
# to be installed.
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitelib}:$PYTHONPATH" %{__python2} test/suite.py
%if %{with python3}
pushd %{py3dir}
PYTHONPATH="$RPM_BUILD_ROOT%{python3_sitelib}:$PYTHONPATH" %{__python3} test/suite.py
popd
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files -n python2-pyasn1
%defattr(-,root,root,-)
%doc README.txt doc/*.html
%license LICENSE.txt
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}-*.egg-info/

%files -n python2-pyasn1-modules
%defattr(-,root,root,-)
%{python_sitelib}/%{module}_modules/
%{python_sitelib}/%{module}_modules-%{modules_version}-*.egg-info/

%if 0%{?with_python3}
%files -n python3-pyasn1
%defattr(-,root,root,-)
%doc README.txt doc/*.html
%license LICENSE.txt
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-%{version}-*.egg-info/

%files -n python3-pyasn1-modules
%defattr(-,root,root,-)
%{python3_sitelib}/%{module}_modules/
%{python3_sitelib}/%{module}_modules-%{modules_version}-*.egg-info/
%endif

%changelog
* Mon May 23 2016 Jan Cholasta <jcholast@redhat.com> - 0.1.9-7
- Add missing Obsoletes on old package names

* Tue May  3 2016 Jan Cholasta <jcholast@redhat.com> - 0.1.9-6
- Set version and release in python- Provides

* Tue Apr 26 2016 Jan Cholasta <jcholast@redhat.com> - 0.1.9-5.1
- Update to upstream 0.1.9, modules 0.0.8

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.1.6-2
- Mass rebuild 2013-12-27

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 0.1.6-1
- update to upstream release 0.1.6
- update modules to 0.0.4
- update description
- add python3-pyasn1 subpackage
- add versioned Requires for the module subpackages
- add %%check section

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 02 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 0.1.2-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Rob Crittenden <rcritten@redhat.com> - 0.0.12a-1
- Update to upstream version 0.0.12a

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.0.9a-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 16 2009 Rob Crittenden <rcritten@redhat.com> - 0.0.9a-1
- Update to upstream version 0.0.9a
- Include patch that adds parsing for the Any type

* Wed Sep  2 2009 Rob Crittenden <rcritten@redhat.com> - 0.0.8a-5
- Include doc/notes.html in the package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.0.8a-2
- Rebuild for Python 2.6

* Tue Sep  9 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.0.8a-1
- Update to upstream version 0.0.8a

* Wed Jan 16 2008 Rob Crittenden <rcritten@redhat.com> - 0.0.7a-4
- Use setuptools to install the package
- simplify the files included in the rpm so it includes the .egg-info

* Mon Jan 14 2008 Rob Crittenden <rcritten@redhat.com> - 0.0.7a-3
- Rename to python-pyasn1
- Spec file cleanups

* Mon Nov 19 2007 Karl MacMillan <kmacmill@redhat.com> - 0.0.7a-2
- Update rpm to be more fedora friendly

* Thu Nov 8 2007 Simo Sorce <ssorce@redhat.com> 0.0.7a-1
- New release

* Mon May 28 2007 Andreas Hasenack <andreas@mandriva.com> 0.0.6a-1mdv2008.0
+ Revision: 31989
- fixed (build)requires
- Import pyasn1

