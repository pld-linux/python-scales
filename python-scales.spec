#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	scales
Summary:	Stats for Python processes
Summary(pl.UTF-8):	Statystyki dla procesów Pythona
Name:		python-%{module}
Version:	1.0.9
Release:	13
License:	Apache
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/s/scales/%{module}-%{version}.tar.gz
# Source0-md5:	c61167f2b5f506f0a34a7b8a295a9567
Patch0:		python-3.8.patch
URL:		https://www.github.com/Cue/scales
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-nose
BuildRequires:	python-setuptools > 1:7.0
BuildRequires:	python-six
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools > 1:7.0
BuildRequires:	python3-six
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tracks server state and statistics, allowing you to see what your
server is doing. It can also send metrics to Graphite for graphing or
to a file for crash forensics.

%description -l pl.UTF-8
Ten moduł śledzi stan serwera i jego statystyki, pozwalając zobaczyć,
co serwer robi. Potrafi także wysyłać dane do Graphite do wykresów
albo do pliku do analizy.

%package -n python3-%{module}
Summary:	Stats for Python processes
Summary(pl.UTF-8):	Statystyki dla procesów Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
Tracks server state and statistics, allowing you to see what your
server is doing. It can also send metrics to Graphite for graphing or
to a file for crash forensics.

%description -n python3-%{module} -l pl.UTF-8
Ten moduł śledzi stan serwera i jego statystyki, pozwalając zobaczyć,
co serwer robi. Potrafi także wysyłać dane do Graphite do wykresów
albo do pliku do analizy.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/greplin
%dir %{py_sitescriptdir}/greplin/scales
%{py_sitescriptdir}/greplin/scales/*.py[co]
%{py_sitescriptdir}/scales-%{version}-py*.egg-info
%{py_sitescriptdir}/scales-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%dir %{py3_sitescriptdir}/greplin
%{py3_sitescriptdir}/greplin/scales
%{py3_sitescriptdir}/scales-%{version}-py*.egg-info
%{py3_sitescriptdir}/scales-%{version}-py*-nspkg.pth
%endif
