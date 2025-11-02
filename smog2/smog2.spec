%global debug_package %{nil}
Name:           smog2
Version:        2.5
Release:        1%{?dist}
Summary:        SMOG2 - A tool for molecular simulation

License:        GPLv2
URL:            https://smog-server.org/smog2/
Source0:        https://smog-server.org/smog2/code/smog-2.5.tgz

BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-CPAN
BuildRequires:  zlib-devel

Requires:       perl

%description
SMOG2 (Structure and Mechanics of Geometries) is a tool for molecular simulation and analysis. This package integrates the SMOG2 toolkit into the MDSPACE environment.

%prep
%autosetup -n smog-%{version}

%build
export PERL5LIB=%{_builddir}/perl5/lib/perl5
export PATH=%{_builddir}/perl5/bin:$PATH
export PERL_MM_OPT="INSTALL_BASE=%{_builddir}/perl5"
export PERL_LOCAL_LIB_ROOT=%{_builddir}/perl5

perl -MCPAN -e 'install local::lib'
eval $(perl -I$HOME/perl5/lib/perl5/ -Mlocal::lib)

cpanm --notest XML::Validator::Schema

echo -n '#!/bin/bash' > configure
echo "" >> configure
cat configure.smog2 >> configure
chmod 777 configure
./configure

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/smog2 %{buildroot}/usr/bin/

mkdir -p %{buildroot}/perl5/lib/perl5
cp -r %{_builddir}/perl5/lib/perl5/* %{buildroot}/perl5/lib/perl5/

%files
%{_bindir}/smog2
/perl5/lib/perl5/*

%changelog
* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr>
- Initial build for SMOG2 molecular simulation toolkit
