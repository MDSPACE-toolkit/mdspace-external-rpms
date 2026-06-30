%global debug_package %{nil}

Name:           rtb2
Version:        1.0.0
Release:        1%{?dist}
Summary:        RTB2 - Rotation-Translation Block normal mode analysis tools

License:        Proprietary
URL:            https://github.com/MDSPACE-toolkit/rtb2
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  blas-devel
BuildRequires:  arpack-devel
BuildRequires:  flexiblas-devel

Requires:       perl
Requires:       flexiblas
Requires:       flexiblas-netlib

%description
RTB2 provides tools for rotation-translation block normal mode analysis.
This package installs the RTB2 binaries and the makebloc.pl helper script.

%prep
%autosetup -n %{name}-%{version}

%ifarch x86_64
%global safe_arch_flags -march=x86-64 -mtune=generic
%else
%global safe_arch_flags %{nil}
%endif

%build
cd src
mkdir -p build
cd build
export CC=gcc
export CXX=g++
export FC=gfortran
export F77=gfortran
export CFLAGS="%{optflags} %{safe_arch_flags}"
export CXXFLAGS="%{optflags} %{safe_arch_flags}"
export FFLAGS="%{optflags} %{safe_arch_flags}"
export FCFLAGS="%{optflags} %{safe_arch_flags}"
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix}

make

%install
mkdir -p %{buildroot}%{_bindir}

install -m 0755 src/build/rtb2 %{buildroot}%{_bindir}/rtb2
install -m 0755 scripts/makebloc.pl %{buildroot}%{_bindir}/makebloc.pl

%files
%{_bindir}/rtb2
%{_bindir}/makebloc.pl

%changelog
* Tue May 26 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 1.0.0-1
- Initial package build for RTB2.
