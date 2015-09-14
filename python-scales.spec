#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	scales
Summary:	Stats for Python processes
Summary(pl.UTF-8):	Statyski dla procesów Pythona
Name:		python-%{module}
Version:	1.0.9
Release:	3
License:	Apache
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/s/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	c61167f2b5f506f0a34a7b8a295a9567
URL:		https://www.github.com/Cue/scales
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-nose
BuildRequires:	python-setuptools > 7.0
BuildRequires:	python-six
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools > 7.0
BuildRequires:	python3-six
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tracks server state and statistics, allowing you to see what your
server is doing. It can also send metrics to Graphite for graphing or
to a file for crash forensics.

%description -l pl.UTF-8
Śledzi stan serwerqa i jego statystyki pozwalając zobaczyć co serwer
robi. Pozwala wysłać dane do Graphite albo do pliku do analizy.

%package -n python3-%{module}
Summary:	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Tracks server state and statistics, allowing you to see what your
server is doing. It can also send metrics to Graphite for graphing or
to a file for crash forensics.

%description -n python3-%{module} -l pl.UTF-8
Śledzi stan serwerqa i jego statystyki pozwalając zobaczyć co serwer
robi. Pozwala wysłać dane do Graphite albo do pliku do analizy.

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

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
