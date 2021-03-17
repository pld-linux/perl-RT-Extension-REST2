#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	RT
%define		pnam	Extension-REST2
Summary:	RT::Extension::REST2 - Adds a modern REST API to RT under /REST/2.0/
Name:		perl-RT-Extension-REST2
Version:	1.11
Release:	1
License:	GPL v2
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/RT/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	a06ea24fcd25e57612b482054d51d977
URL:		https://metacpan.org/release/RT-Extension-REST2
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Adds a modern REST API to RT under /REST/2.0/.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

sed -i -e 's#^my $lib_path =.*#my $lib_path = "%{perl_vendorlib}/RT";#g' Makefile.PL
sed -i -e 's#^my $sbin_path =.*#my $sbin_path = "%{_sbindir}";#g' Makefile.PL
sed -i -e 's#^my $bin_path =.*#my $bin_path = "%{_bindir}";#g' Makefile.PL

%build

%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{perl_vendorlib}/RT/Extension/
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/RT-Extension-REST2/lib/RT/Extension/* $RPM_BUILD_ROOT%{perl_vendorlib}/RT/Extension/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README TODO
%{perl_vendorlib}/RT/Extension/REST2
%{perl_vendorlib}/RT/Extension/REST2.pm
%{_mandir}/man3/RT::Extension::REST2.3*
%{_mandir}/man3/RT::Extension::REST2::Util.3*
