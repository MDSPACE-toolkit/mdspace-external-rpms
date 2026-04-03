%global debug_package %{nil}
%undefine __cmake_in_source_build

# State Nov 11 2020, LTO causes
# TestXMLHyperTreeGridIO.cxx.o (symbol from plugin): undefined reference to symbol
# '_ZZNSt8__detail18__to_chars_10_implIjEEvPcjT_E8__digits@@LLVM_11'
%global _lto_cflags %{nil}

%bcond_with OSMesa
%bcond_with java
%bcond_with mpich
%bcond_with openmpi
%bcond_with xdummy

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%bcond_without flexiblas
%endif

# VTK currently is carrying local modifications to gl2ps
%bcond_with gl2ps

# VTK currently requires unreleased fmt 8.1.0
%bcond_with fmt

Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 9.1.0
Release: 19%{?dist}
License: BSD
Source0: https://www.vtk.org/files/release/9.1/VTK-%{version}.tar.gz
# Patch required libharu version (Fedora 33+ contains the needed VTK patches)
Patch0: vtk-libharu.patch
# Upstream patch to link kissfft with libm
Patch1: vtk-kissfft-libm.patch
# Upstream patch to support netcdf 4.9.0
# https://gitlab.kitware.com/vtk/vtk/-/issues/18576
Patch2: vtk-netcdf.patch
# Duplicate define conflict with Xutil, see:
# https://gitlab.kitware.com/vtk/vtk/-/issues/18048
Patch3: vtk-AllValues.patch
# CVE-2021-42521 - vtkXMLTreeReader: possible nullptr dereference
Patch4: https://gitlab.kitware.com/vtk/vtk/-/merge_requests/9621.patch

URL: https://vtk.org/

BuildRequires:  cmake
%global cmake_gen %{nil}
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
%if %{with flexiblas}
BuildRequires:  flexiblas-devel
%else
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
%endif
BuildRequires:  boost-devel
BuildRequires:  cgnslib-devel
BuildRequires:  cli11-devel
BuildRequires:  double-conversion-devel
BuildRequires:  eigen3-devel
BuildRequires:  expat-devel
%if %{with fmt}
BuildRequires:  fmt-devel >= 8.1.0
%endif
BuildRequires:  freetype-devel
%if %{with gl2ps}
BuildRequires:  gl2ps-devel
%endif
BuildRequires:  glew-devel
BuildRequires:  hdf5-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  libarchive-devel
BuildRequires:  libGL-devel
BuildRequires:  libharu-devel >= 2.3.0-9
BuildRequires:  libICE-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libogg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtheora-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXt-devel
BuildRequires:  lz4-devel
%{?with_OSMesa:BuildRequires: mesa-libOSMesa-devel}
BuildRequires:  netcdf-cxx-devel
BuildRequires:  pugixml-devel
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
BuildRequires:  sqlite-devel
BuildRequires:  utf8cpp-devel
BuildRequires:  zlib-devel
BuildRequires:  PEGTL-devel
BuildRequires:  cmake(Qt6Quick)

Requires: hdf5 = %{_hdf5_version}

%global vtk_devel_requires \
Requires: cmake \
%if %{with flexiblas} \
Requires: flexiblas-devel%{?_isa} \
%else \
Requires: blas-devel%{?_isa} \
Requires: lapack-devel%{?_isa} \
%endif \
Requires: boost-devel%{?_isa} \
Requires: cgnslib-devel%{?_isa} \
Requires: cli11-static \
Requires: double-conversion-devel%{?_isa} \
Requires: eigen3-static \
Requires: expat-devel%{?_isa} \
%if %{with fmt} \
Requires: fmt-devel%{?_isa} \
%endif \
Requires: freetype-devel%{?_isa} \
%if %{with gl2ps} \
Requires: gl2ps-devel%{?_isa} \
%endif \
Requires: glew-devel%{?_isa} \
Requires: jsoncpp-devel%{?_isa} \
Requires: libarchive-devel%{?_isa} \
Requires: libGL-devel%{?_isa} \
Requires: libharu-devel%{?_isa} >= 2.3.0-9 \
Requires: libjpeg-devel%{?_isa} \
Requires: libogg-devel%{?_isa} \
Requires: libpng-devel%{?_isa} \
Requires: libtheora-devel%{?_isa} \
Requires: libtiff-devel%{?_isa} \
Requires: libxml2-devel%{?_isa} \
Requires: libX11-devel%{?_isa} \
Requires: libXext-devel%{?_isa} \
Requires: libXt-devel%{?_isa} \
Requires: lz4-devel%{?_isa} \
%if %{with OSMesa} \
Requires: mesa-libOSMesa-devel%{?_isa} \
%endif \
Requires: netcdf-cxx-devel%{?_isa} \
Requires: pugixml-devel%{?_isa} \
Requires: sqlite-devel%{?_isa} \
Requires: cmake(Qt6Core) \
Requires: cmake(Qt6Gui) \
Requires: cmake(Qt6Widgets) \
Requires: cmake(Qt6OpenGL) \
Requires: cmake(Qt6OpenGLWidgets) \
Requires: utf8cpp-devel \
Requires: zlib-devel%{?_isa} \
Requires: PEGTL-devel%{?_isa} \
Requires: cmake(Qt6Quick) \

Provides: bundled(kwsys-base64)
Provides: bundled(kwsys-commandlinearguments)
Provides: bundled(kwsys-directory)
Provides: bundled(kwsys-dynamicloader)
Provides: bundled(kwsys-encoding)
Provides: bundled(kwsys-fstream)
Provides: bundled(kwsys-fundamentaltype)
Provides: bundled(kwsys-glob)
Provides: bundled(kwsys-md5)
Provides: bundled(kwsys-process)
Provides: bundled(kwsys-regularexpression)
Provides: bundled(kwsys-status)
Provides: bundled(kwsys-system)
Provides: bundled(kwsys-systeminformation)
Provides: bundled(kwsys-systemtools)
Provides: bundled(diy2)
Provides: bundled(exodusII) = 2.0.0
Provides: bundled(exprtk) = 2.71
%if !%{with fmt}
Provides: bundled(fmt) = 8.1.0
%endif
Provides: bundled(ftgl) = 1.32
%if !%{with gl2ps}
Provides: bundled(gl2ps) = 1.4.0
%endif
Provides: bundled(ioss) = 20210512
Provides: bundled(kissfft)
Provides: bundled(metaio)
Provides: bundled(verdict) = 1.2.0
Provides: bundled(vpic)
Provides: bundled(xdmf2) = 2.1
Provides: bundled(xdmf3)

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

This build is provided without MPI, Java, Python, tests, examples, and docs.

%package devel
Summary: VTK header files for building C++ code
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: hdf5-devel%{?_isa}
%{vtk_devel_requires}

%description devel
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

%package qt
Summary: Qt bindings for VTK
Requires: %{name}%{?_isa} = %{version}-%{release}

%description qt
Qt bindings for VTK.

%prep
PATCH_DIR=%{SOURCE0}/patches
%autosetup -p1 -n VTK-%{version}

for x in vtk{cli11,doubleconversion,eigen,expat,%{?with_fmt:fmt,}freetype,%{?with_gl2ps:gl2ps,}glew,hdf5,jpeg,jsoncpp,libharu,libxml2,lz4,lzma,netcdf,ogg,pegtl,png,pugixml,sqlite,theora,tiff,utf8,zfp,zlib}
do
  rm -r ThirdParty/*/${x}
done

find Utilities/KWSys/vtksys/ -name \*.[ch]\* | grep -vE '^Utilities/KWSys/vtksys/([a-z].*|Configure|SharedForward|Status|String\.hxx|Base64|CommandLineArguments|Directory|DynamicLoader|Encoding|FStream|FundamentalType|Glob|MD5|Process|RegularExpression|System|SystemInformation|SystemTools)(C|CXX|UNIX)?\.' | xargs rm

%build
export CFLAGS="%{optflags} -D_UNICODE -DHAVE_UINTPTR_T"
export CXXFLAGS="%{optflags} -D_UNICODE -DHAVE_UINTPTR_T"

%global vtk_cmake_options \\\
 -DCMAKE_INSTALL_DOCDIR=share/doc/%{name} \\\
 -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \\\
 -DCMAKE_INSTALL_LICENSEDIR:PATH=share/licenses/%{name} \\\
 -DVTK_CUSTOM_LIBRARY_SUFFIX="" \\\
 -DVTK_VERSIONED_INSTALL:BOOL=OFF \\\
 -DVTK_GROUP_ENABLE_Imaging:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Qt:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Rendering:STRING=YES \\\
 -DVTK_GROUP_ENABLE_StandAlone:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Views:STRING=YES \\\
 -DVTK_MODULE_USE_EXTERNAL_VTK_libproj:BOOL=OFF \\\
 -DVTK_GROUP_ENABLE_Web:STRING=NO \\\
 -DVTK_MODULE_ENABLE_VTK_CommonArchive:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_DomainsMicroscopy:STRING=NO \\\
 -DVTK_MODULE_ENABLE_VTK_GUISupportQtQuick:STRING=NO \\\
 -DVTK_BUILD_QML_PLUGIN:BOOL=OFF \\\
 -DVTK_MODULE_ENABLE_VTK_GeovisGDAL:STRING=NO \\\
 -DVTK_MODULE_ENABLE_VTK_ImagingOpenGL2:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_InfovisBoost:STRING=NO \\\
 -DVTK_MODULE_ENABLE_VTK_InfovisBoostGraphAlgorithms:STRING=NO \\\
 -DVTK_MODULE_ENABLE_VTK_IOMySQL:STRING=NO \\\
 -DVTK_WRAP_JAVA:BOOL=OFF \\\
 -DVTK_WRAP_PYTHON:BOOL=OFF \\\
 -DVTK_USE_EXTERNAL=ON \\\
%if !%{with fmt} \
 -DVTK_MODULE_USE_EXTERNAL_VTK_fmt:BOOL=OFF \\\
%endif \
%if !%{with gl2ps} \
 -DVTK_MODULE_USE_EXTERNAL_VTK_gl2ps:BOOL=OFF \\\
%endif \
 -DVTK_MODULE_USE_EXTERNAL_VTK_exprtk:BOOL=OFF \\\
 -DVTK_MODULE_USE_EXTERNAL_VTK_ioss:BOOL=OFF \\\
 -DVTK_USE_TK=OFF \\\
 %{?with_flexiblas:-DBLA_VENDOR=FlexiBLAS}

%global _vpath_builddir build
%cmake %{cmake_gen} \
 %{vtk_cmake_options} \
 -DVTK_BUILD_DOCUMENTATION:BOOL=OFF \
 -DVTK_BUILD_EXAMPLES:BOOL=OFF \
 -DVTK_BUILD_TESTING:BOOL=OFF
%cmake_build

find . -name \*.c -or -name \*.cxx -or -name \*.h -or -name \*.hxx -or \
       -name \*.gif | xargs chmod -x

rm -rf %{buildroot}%{_libdir}/qml/VTK.9.1

%install
%global _vpath_builddir build
%cmake_install

rm -f \
  %{buildroot}%{_bindir}/vtkParseJava \
  %{buildroot}%{_bindir}/vtkWrapJava \
  %{buildroot}%{_bindir}/vtkWrapPython \
  %{buildroot}%{_bindir}/vtkWrapPythonInit

pushd build
ls %{buildroot}%{_libdir}/*.so.* \
  | grep -Ev '(Java|Python)' | sed -e's,^%{buildroot},,' > libs.list
popd

for file in `find %{buildroot} -type f -perm 0755 \
  | xargs -r file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done

find %{buildroot} -type f -name "*.a" -delete
find %{buildroot} -type f -name "*.la" -delete

%files -f build/libs.list
%license %{_defaultlicensedir}/%{name}/
%doc README.md

%files devel
%doc Utilities/Upgrading
%{_bindir}/vtkProbeOpenGLVersion
%{_bindir}/vtkWrapHierarchy
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/hierarchy/

%files qt
%{_libdir}/lib*Qt*.so.*

%changelog
* Wed Nov 19 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 9.1.0-19
- Port to Qt6
