%global debug_package %{nil}
%global _lto_cflags %{nil}
Name:           genesis-nompi
Version:        2.1.6.3
Release:        0%{?dist}
Summary:        GENESIS molecular dynamics simulation engine without MPI

License:        GPLv2
URL:            https://github.com/MDSPACE-toolkit/mdspace-genesis
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  fftw-devel
BuildRequires:  zlib-devel
BuildRequires:  lapack-devel
BuildRequires:  blas-devel

# Both variants install the same GENESIS executables.
Conflicts:      genesis

%description
GENESIS (Generalized-Ensemble Simulation System) is a high-performance molecular
dynamics simulation package designed for biomolecular systems. This build is
configured with --disable-mpi and does not require an MPI implementation.

%prep
%autosetup -n mdspace-genesis-%{version}

%build
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export FFLAGS="%{build_fflags} -fallow-argument-mismatch"
export FCFLAGS="%{build_fflags} -fallow-argument-mismatch"
autoreconf -fi
FC=gfortran \
CC=gcc \
CXX=g++ \
./configure --prefix=%{_prefix} --disable-mpi
make

%install
make install DESTDIR=%{buildroot}

%files
%{_bindir}/*

%changelog
* Wed Oct 21 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 2.1.6.3-0
- Add serial GENESIS build with --disable-mpi
