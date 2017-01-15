%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-gpgauth
Version:        0.1
Release:        1%{?dist}
Summary:        a python library for GPG-based challenge/response 2-factor authentication in web applications
Group:          Development/Languages

License:        Tequilaware
URL:            https://github.com/charliewolf/python-gpgauth
Source0:        https://github.com/charliewolf/%{name}/archive/%{version}.tar.gz
BuildArch:      noarch

%description
a python library for GPG-based challenge/response 2-factor authentication in web applications

%package -n     python2-gpgauth
Summary:        a python library for GPG-based challenge/response 2-factor authentication in web applications
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       gnupg
Requires:       python2-gnupg
%{?python_provide:%python_provide python2-gpgauth}
%{?el6:Provides: python-gpgauth}
%{?el6:Obsoletes: python-gpgauth < 0.3.8}

%description -n python2-gpgauth
a python library for GPG-based challenge/response 2-factor authentication in web applications

%if %{with python3}
%package -n     python3-gpgauth
Summary:        a python library for GPG-based challenge/response 2-factor authentication in web applications
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       gnupg
Requires:       python3-gnupg
%{?python_provide:%python_provide python3-gpgauth}

%description -n python3-gpgauth
a python library for GPG-based challenge/response 2-factor authentication in web applications
%endif # with python3

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build
%if %{with python3}
%py3_build
%endif # with python3

%install
%py2_install
%if %{with python3}
%py3_install
%endif # with python3

%files -n python2-gpgauth
%{!?_licensedir:%global license %doc}
%doc README.txt
%license LICENSE.txt
%{python2_sitelib}/gpgauth
%{python2_sitelib}/gpgauth-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-gpgauth
%doc README.txt
%license LICENSE.txt
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/gpgauth
%{python3_sitelib}/gpgauth-%{version}-py?.?.egg-info
%endif # with python3

%changelog
* Sat Jan 14 2017 Charlie Wolf <charlie@wolf.is> - 0.1-1
- Initial package

