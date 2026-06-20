%global debug_package %{nil}
Name:           genesis
Version:        2.1.6.2
Release:        0%{?dist}
Summary:        GENESIS molecular dynamics simulation engine

License:        GPLv2
URL:            https://github.com/MDSPACE-toolkit/mdspace-genesis
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  openmpi-devel
BuildRequires:  fftw-devel
BuildRequires:  zlib-devel
BuildRequires:  blas-devel
BuildRequires:  lapack-devel

Requires:       openmpi
Provides: libmpi.so.40()(64bit)
Provides: libmpi_mpifh.so.40()(64bit)
Provides: libmpi_usempi_ignore_tkr.so.40()(64bit)
Provides: libmpi_usempif08.so.40()(64bit)

%description
GENESIS (Generalized-Ensemble Simulation System) is a high-performance molecular
dynamics simulation package designed for biomolecular systems. This build is
compatible with MDSPACE and includes the required Fortran configuration flags.

%prep
%autosetup -n mdspace-genesis-%{version}

%ifarch x86_64
%global safe_arch_flags -march=x86-64 -mtune=generic
%else
%global safe_arch_flags %{nil}
%endif

%build
export PATH="%{_libdir}/openmpi/bin:$PATH"
export LD_LIBRARY_PATH="%{_libdir}/openmpi/lib:${LD_LIBRARY_PATH:-}"

export CFLAGS="%{optflags} %{safe_arch_flags}"
export CXXFLAGS="%{optflags} %{safe_arch_flags}"
export FFLAGS="%{optflags} %{safe_arch_flags} -fallow-argument-mismatch -ffree-line-length-none"
export FCFLAGS="%{optflags} %{safe_arch_flags} -fallow-argument-mismatch -ffree-line-length-none"

autoreconf -fi
FC=mpif90 \
CC=mpicc \
CXX=mpicxx \
./configure --prefix=/usr
make

%install
export PATH="%{_libdir}/openmpi/bin:$PATH"
export LD_LIBRARY_PATH="%{_libdir}/openmpi/lib:${LD_LIBRARY_PATH:-}"
make install DESTDIR=%{buildroot}

%files
%{_bindir}/*

%changelog
* Mon Dec 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 2.6.0-0
- Update to GENESIS 2.1.6
* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 1.4.0-1
- Initial GENESIS build for MDSPACE integration
