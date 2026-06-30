%global debug_package %{nil}

%ifarch x86_64
%global safe_arch_flags -march=x86-64 -mtune=generic
%global elnemo_arch_flags -m64 -mcmodel=large -fno-pie -no-pie
%else
%global safe_arch_flags %{nil}
%global elnemo_arch_flags -mcmodel=large -fno-pie -no-pie
%endif

Name:           elnemo
Version:        1.0.0
Release:        1%{?dist}
Summary:        ElNemo - Normal Mode Analysis for Biomolecular Systems

License:        GPLv2
URL:            https://github.com/MDSPACE-toolkit/nma
Source0:        %{url}/archive/refs/heads/master.tar.gz

# Build Requirements
BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  fftw-devel
BuildRequires:  openmpi-devel
BuildRequires:  zlib-devel

%description
ElNemo is a software package for normal mode analysis of biomolecular systems.
It is particularly useful for studying the vibrational modes of large biomolecules 
such as proteins and nucleic acids. This build provides a functional installation 
for the package from the source code.

%prep
%autosetup -n nma-master
sed -i 's/[[:space:]]-m64//g' ElNemo/Makefile

%build
cd ElNemo
export CC=gcc
export CXX=g++
export FC=gfortran
export F77=gfortran
export CFLAGS="%{optflags} %{safe_arch_flags}"
export CXXFLAGS="%{optflags} %{safe_arch_flags}"
export FFLAGS="%{optflags} %{safe_arch_flags}"
export FCFLAGS="%{optflags} %{safe_arch_flags}"
make FC=gfortran FFLAGS="-O3 %{safe_arch_flags} %{elnemo_arch_flags}"

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 ElNemo/nma_diagrtb %{buildroot}%{_bindir}/
install -m 0755 ElNemo/nma_check_modes %{buildroot}%{_bindir}/
install -m 0755 ElNemo/nma_elnemo_pdbmat %{buildroot}%{_bindir}/

%files
%{_bindir}/nma_diagrtb
%{_bindir}/nma_check_modes
%{_bindir}/nma_elnemo_pdbmat

%changelog
* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 1.0.0-1
- Initial package build for ElNemo.
