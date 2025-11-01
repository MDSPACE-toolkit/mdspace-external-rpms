%global debug_package %{nil}
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

%build
cd ElNemo
make

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
