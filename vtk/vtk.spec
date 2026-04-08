%global debug_package %{nil}
%undefine __cmake_in_source_build

Name:           vtk-qt6-lean
Version:        9.6.1
Release:        1%{?dist}
Summary:        Minimal VTK build with Qt6 support
License:        BSD
URL:            https://vtk.org/
Source0:        https://www.vtk.org/files/release/9.6/VTK-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXt-devel
BuildRequires:  eigen3-devel
BuildRequires:  libxkbcommon-devel

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative

%description
Minimal VTK package built with Qt6 support for QWidget-based applications.
This package intentionally enables only a small subset of VTK modules.

%prep
%autosetup -n VTK-%{version}

%build
%cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_INCLUDEDIR=include \
  -DINCLUDE_INSTALL_DIR=include \
  -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DBUILD_SHARED_LIBS=ON \
  -DVTK_BUILD_TESTING=OFF \
  -DVTK_BUILD_EXAMPLES=OFF \
  -DVTK_BUILD_DOCUMENTATION=OFF \
  -DVTK_WRAP_PYTHON=OFF \
  -DVTK_WRAP_JAVA=OFF \
  -DVTK_GROUP_ENABLE_Qt=YES \
  -DVTK_QT_VERSION=6 \
  -DVTK_MODULE_ENABLE_VTK_GUISupportQt=YES \
  -DVTK_MODULE_ENABLE_VTK_RenderingQt=YES \
  -DVTK_MODULE_ENABLE_VTK_ViewsQt=YES \
  -DVTK_MODULE_ENABLE_VTK_GUISupportQtQuick=NO \
  -DVTK_MODULE_ENABLE_VTK_GUISupportQtSQL=NO \
  -DVTK_GROUP_ENABLE_StandAlone=WANT \
  -DVTK_MODULE_ENABLE_VTK_CommonCore=YES \
  -DVTK_MODULE_ENABLE_VTK_CommonDataModel=YES \
  -DVTK_MODULE_ENABLE_VTK_CommonExecutionModel=YES \
  -DVTK_MODULE_ENABLE_VTK_RenderingCore=YES \
  -DVTK_MODULE_ENABLE_VTK_RenderingOpenGL2=YES \
  -DVTK_MODULE_ENABLE_VTK_InteractionStyle=YES \
  -DVTK_MODULE_ENABLE_VTK_FiltersSources=YES \
  -DVTK_MODULE_ENABLE_VTK_RenderingUI=YES

%cmake_build

%install
%cmake_install

%files
%license %{_datadir}/licenses/VTK/*
%{_datadir}/vtk-9.6/*
%{_includedir}/*
%{_libdir}/*
%{_bindir}/*

%changelog
* Tue Apr 07 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 9.6.1-1
- Minimal VTK Qt6 build for EL9
