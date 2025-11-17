%global debug_package %{nil}
Name:           xmipp
Version:        3.25.06.0
Release:        2%{?dist}
Summary:        XMIPP - Image Processing Software for CryoEM

License:        GPL
URL:            https://xmipp.cnb.csic.es/
Source0:        https://github.com/I2PC/xmipp/archive/refs/tags/v3.25.06.0-Rhea.tar.gz

BuildRequires:  gcc-c++, make, cmake, perl, fftw3-devel, libtiff-devel, mpi-devel, nvidia-driver
Requires:       fftw3, libtiff, mpi, nvidia-driver
Provides: libmpi.so.40()(64bit), libsvm.so()(64bit), libcuFFTAdvisor.so()(64bit), libmpi_cxx.so.40()(64bit)

%description
XMIPP is a software suite designed for image processing in cryo-electron microscopy (cryo-EM). 
It includes a range of tools for working with cryo-EM images and maps.

%prep
%autosetup -n xmipp-%{version}-Rhea

%build
./xmipp getSources
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_BUILD_TYPE=Release -DXMIPP_LINK_TO_SCIPION=NO
make -j$(nproc)

%install
cd build
make install DESTDIR=%{buildroot}
find %{buildroot}/usr/bin -type f -exec sed -i '1s|^#!.*python$|#!/usr/bin/env python3|' {} \;
find %{buildroot}/usr/bin -type f -name "*.py" -exec chmod +x {} \;
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
* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr>
- Initial package for XMIPP
