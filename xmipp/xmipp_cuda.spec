%global debug_package %{nil}

Name:           xmipp-cuda
Version:        3.25.06.0
Release:        3%{?dist}
Summary:        XMIPP - Image Processing Software for CryoEM

License:        GPL
URL:            https://xmipp.cnb.csic.es/
Source0:        https://github.com/I2PC/xmipp/archive/refs/tags/v%{version}-Rhea.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  perl
BuildRequires:  fftw3-devel
BuildRequires:  libtiff-devel
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
%autosetup -n xmipp3-%{version}-Rhea

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
  -DCMAKE_CUDA_ARCHITECTURES=86
make -j$(nproc)
popd

%install
rm -rf %{buildroot}

pushd build
make install DESTDIR=%{buildroot}
popd

if [ -d "%{buildroot}%{_bindir}" ]; then
  find %{buildroot}%{_bindir} -type f -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \; || true
  find %{buildroot}%{_bindir} -type f -name "*.py" -exec chmod +x {} \; || true
fi
if [ -d "%{buildroot}%{_libexecdir}/xmipp" ]; then
  find %{buildroot}%{_libexecdir}/xmipp -type f -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \; || true
  find %{buildroot}%{_libexecdir}/xmipp -type f -name "*.py" -exec chmod +x {} \; || true
fi

rm -rf %{buildroot}/usr/include/gtest
rm -rf %{buildroot}/usr/include/gmock

%files
%{_bindir}/*
/usr/lib/*
/usr/bindings/*
/usr/resources/*
/usr/pylib/*
/usr/xmipp.bashrc
%{_includedir}/*
%{_datadir}/*

%changelog
* Thu Feb 17 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr>
- Make PMI, CUDA subpackages
* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr>
- Initial package for XMIPP
