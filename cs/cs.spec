%global debug_package %{nil}
%global __strip /bin/true
Name:           cryosparc-cs-reader
Version:        1.0.0
Release:        1%{?dist}
Summary:        CryoSPARC .cs metadata reader for MDSPACE

License:        GPL-3.0-or-later
URL:            https://github.com/MDSPACE-toolkit/cs_reader
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  patchelf
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-pip

Requires:       glibc
Requires:       libgcc
Requires:       libstdc++

%description
cryosparc-cs-reader converts CryoSPARC .cs particle metadata into an
MDSPACE-compatible TSV file.

The executable is compiled with Nuitka and contains its Python runtime and
required Python modules. Python is not required when running the installed
program.

%prep
%autosetup -n cs_reader-%{version}

%build
python3 -m venv build-venv

build-venv/bin/python -m pip install --upgrade pip

build-venv/bin/python -m pip install \
    nuitka \
    ordered-set \
    zstandard \
    numpy \
    cryosparc-tools

build-venv/bin/python -m nuitka \
    --standalone \
    --deployment \
    --static-libpython=no \
    --output-dir=build-nuitka \
    --output-filename=cryosparc-cs-reader \
    --include-package=cryosparc \
    --include-package-data=cryosparc \
    --include-package=numpy \
    cs_reader.py

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libexecdir}/cryosparc-cs-reader
install -d %{buildroot}%{_bindir}

cp -a \
    build-nuitka/cs_reader.dist/. \
    %{buildroot}%{_libexecdir}/cryosparc-cs-reader/

ln -s \
    ../libexec/cryosparc-cs-reader/cryosparc-cs-reader \
    %{buildroot}%{_bindir}/cryosparc-cs-reader

%check
export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset PYTHONHOME

%{buildroot}%{_libexecdir}/cryosparc-cs-reader/cryosparc-cs-reader --help
%{buildroot}%{_bindir}/cryosparc-cs-reader --help

%files
%{_bindir}/cryosparc-cs-reader
%{_libexecdir}/cryosparc-cs-reader/

%changelog
* Mon Jul 13 2026 Benjamin Gallois - 1.0.0-1
- Initial RPM package
