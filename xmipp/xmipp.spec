%global debug_package %{nil}

Name:           xmipp
Version:        3.25.06.0
Release:        4%{?dist}
Summary:        XMIPP - Image Processing Software for CryoEM

License:        GPL
URL:            https://xmipp.cnb.csic.es/
Source0:        https://github.com/I2PC/xmipp/archive/refs/tags/v%{version}-Rhea.tar.gz
Patch0:         xmipp-aarch64-cpuid.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  git
BuildRequires:  zlib-devel
BuildRequires:  fftw-devel
BuildRequires:  hdf5-devel
BuildRequires:  sqlite-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  java-11-openjdk-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-numpy

Provides:       libsvm.so()(64bit)

Requires:       fftw3
Requires:       libtiff

Conflicts:      xmipp-cuda
Conflicts:      xmipp-mpi

%description
XMIPP is a software suite designed for image processing in cryo-electron
microscopy (cryo-EM). It includes a range of tools for working with cryo-EM
images and maps.

%prep
%setup -q -n xmipp3-%{version}-Rhea

%ifarch aarch64
%patch -P 0 -p1
%endif

%build
./xmipp getSources

mkdir -p build
pushd build

cmake .. \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_BUILD_TYPE=Release \
  -DXMIPP_LINK_TO_SCIPION=NO \
  -DXMIPP_USE_CUDA=OFF \
  -DXMIPP_USE_MATLAB=OFF \
  -DXMIPP_USE_MPI=OFF \
  -DBUILD_TESTING=OFF \
  -DPython3_EXECUTABLE=%{_bindir}/python3 \
  -DPython3_FIND_STRATEGY=LOCATION \
  -DPython3_ROOT_DIR=%{_prefix}

%make_build

popd

%install
rm -rf %{buildroot}

pushd build
%make_install
popd

if [ -d "%{buildroot}%{_bindir}" ]; then
  find "%{buildroot}%{_bindir}" \
    -type f \
    -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \; \
    || true

  find "%{buildroot}%{_bindir}" \
    -type f \
    -name "*.py" \
    -exec chmod +x {} \; \
    || true
fi

if [ -d "%{buildroot}%{_libexecdir}/xmipp" ]; then
  find "%{buildroot}%{_libexecdir}/xmipp" \
    -type f \
    -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \; \
    || true

  find "%{buildroot}%{_libexecdir}/xmipp" \
    -type f \
    -name "*.py" \
    -exec chmod +x {} \; \
    || true
fi

rm -rf "%{buildroot}%{_includedir}/gtest"
rm -rf "%{buildroot}%{_includedir}/gmock"

%files
%{_bindir}/*
%{_prefix}/lib/*
%{_prefix}/bindings/*
%{_prefix}/resources/*
%{_prefix}/pylib/*
%{_prefix}/xmipp.bashrc
%{_includedir}/*
%{_datadir}/*

%changelog
* Mon Jun 15 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 3.25.06.0-4
- Add an architecture guard around the x86 CPUID implementation.
- Allow XMIPP to compile on AArch64 systems.

* Tue Feb 17 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 3.25.06.0-3
- Add MPI and CUDA subpackages.

* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 3.25.06.0-1
- Initial XMIPP package.
