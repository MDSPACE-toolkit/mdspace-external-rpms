%global debug_package %{nil}

Name:           xmipp-cuda
Version:        3.25.06.0
Release:        4%{?dist}
Summary:        XMIPP - Image Processing Software for CryoEM

License:        GPL
URL:            https://xmipp.cnb.csic.es/
Source0:        https://github.com/I2PC/xmipp/archive/refs/tags/v%{version}-Rhea.tar.gz
Patch0:         xmipp-aarch64-cpuid.patch

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: cmake
BuildRequires: git
BuildRequires: zlib-devel
BuildRequires: fftw-devel
BuildRequires: hdf5-devel
BuildRequires: sqlite-devel
BuildRequires: libtiff-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: java-11-openjdk-devel
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-numpy
BuildRequires: cuda-toolkit-11-7
BuildRequires: cuda-cudart-devel-11-7
BuildRequires: libcufft-devel-11-7

Requires:       fftw3
Requires:       libtiff
Requires:       nvidia-driver

Provides: libsvm.so()(64bit) libcuFFTAdvisor.so()(64bit)

Conflicts: xmipp-mpi
Conflicts: xmipp

%description
XMIPP is a software suite designed for image processing in cryo-electron microscopy (cryo-EM).
It includes a range of tools for working with cryo-EM images and maps.

%prep
%setup -q -n xmipp3-%{version}-Rhea

%ifarch aarch64
%patch -P 0 -p1
%endif

%build
./xmipp getSources

mkdir -p build
pushd build
%global cuda_root /usr/local/cuda-11.7
export CUDA_HOME=/usr/local/cuda-11.7
export PATH=$CUDA_HOME/bin:$PATH
export CPATH=$CUDA_HOME/include${CPATH:+:$CPATH}
export LIBRARY_PATH=$CUDA_HOME/lib64${LIBRARY_PATH:+:$LIBRARY_PATH}
export LD_LIBRARY_PATH=$CUDA_HOME/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
cmake .. \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_BUILD_TYPE=Release \
  -DXMIPP_LINK_TO_SCIPION=NO \
  -DXMIPP_USE_MATLAB=OFF \
  -DXMIPP_USE_MPI=OFF \
  -DXMIPP_USE_CUDA=ON \
  -DBUILD_TESTING=OFF \
  -DPython3_EXECUTABLE=%{_bindir}/python3 \
  -DPython3_FIND_STRATEGY=LOCATION \
  -DPython3_ROOT_DIR=%{_prefix} \
  -DCMAKE_CUDA_ARCHITECTURES=86
%make_build
popd

%install
rm -rf %{buildroot}

pushd build
%make_install
popd

# XMIPP installs its Python modules outside Python's normal search path.  A
# .pth file makes command-line scripts such as xmipp_showj work without
# requiring users to source /usr/xmipp.bashrc first.
install -d "%{buildroot}%{python3_sitelib}"
printf '%s\n' \
  "%{_prefix}/bindings/python" \
  "%{_prefix}/pylib" \
  > "%{buildroot}%{python3_sitelib}/xmipp.pth"

if [ -d "%{buildroot}%{_bindir}" ]; then
  find %{buildroot}%{_bindir} -type f -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \; || true
  find %{buildroot}%{_bindir} -type f -name "*.py" -exec chmod +x {} \; || true
fi
if [ -d "%{buildroot}%{_libexecdir}/xmipp" ]; then
  find %{buildroot}%{_libexecdir}/xmipp -type f -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \; || true
  find %{buildroot}%{_libexecdir}/xmipp -type f -name "*.py" -exec chmod +x {} \; || true
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
%{python3_sitelib}/xmipp.pth
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
