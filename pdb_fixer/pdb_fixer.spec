%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from ^%{_libexecdir}/pdb-fixer/.*$

Name:           pdb-fixer
Version:        1.0.0
Release:        1%{?dist}
Summary:        PDB structure repair tool for MDSPACE

License:        GPL-3.0-or-later
URL:            https://github.com/MDSPACE-toolkit/cs_reader
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  patchelf
BuildRequires:  python3.11
BuildRequires:  python3.11-devel
BuildRequires:  python3.11-pip

Requires:       glibc
Requires:       libgcc
Requires:       libstdc++

%description
pdb-fixer repairs PDB structures using PDBFixer and OpenMM.

It can replace nonstandard residues and optionally add missing residues,
missing atoms, and hydrogens.

The executable is compiled with Nuitka and includes its private Python
runtime and required Python modules. Python is not required at runtime.

%prep
%autosetup -n cs_reader-%{version}

%build
python3.11 -m venv build-venv

build-venv/bin/python -m pip install --upgrade pip

build-venv/bin/python -m pip install \
    nuitka \
    ordered-set \
    zstandard \
    numpy \
    openmm \
    pdbfixer-neoralab

rm -rf build-nuitka

OPENMM_PLUGIN_DIR="$(
    find build-venv \
        -type f \
        -name 'libOpenMMCPU.so' \
        -printf '%h\n' \
        -quit
)"

test -n "${OPENMM_PLUGIN_DIR}"

echo "OpenMM plugin directory: ${OPENMM_PLUGIN_DIR}"
ls -la "${OPENMM_PLUGIN_DIR}"

env \
    CPPFLAGS="" \
    CFLAGS="-O2" \
    CXXFLAGS="-O2" \
    LDFLAGS="" \
    build-venv/bin/python -m nuitka \
        --standalone \
        --deployment \
        --lto=no \
        --static-libpython=no \
        --output-dir=build-nuitka \
        --output-filename=pdb-fixer \
        --include-package=numpy \
        --include-package=openmm \
        --include-package-data=openmm \
        --include-package=pdbfixer \
        --include-package-data=pdbfixer \
        pdb_fixer.py

install -d \
    build-nuitka/pdb_fixer.dist/openmm_plugins

cp -a \
    "${OPENMM_PLUGIN_DIR}/." \
    build-nuitka/pdb_fixer.dist/openmm_plugins/

test -f \
    build-nuitka/pdb_fixer.dist/openmm_plugins/libOpenMMCPU.so

ldd \
    build-nuitka/pdb_fixer.dist/openmm_plugins/libOpenMMCPU.so

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libexecdir}/pdb-fixer
install -d %{buildroot}%{_bindir}

cp -a \
    build-nuitka/pdb_fixer.dist/. \
    %{buildroot}%{_libexecdir}/pdb-fixer/

ln -s \
    ../libexec/pdb-fixer/pdb-fixer \
    %{buildroot}%{_bindir}/pdb-fixer

test -x \
    %{buildroot}%{_libexecdir}/pdb-fixer/pdb-fixer

test -f \
    %{buildroot}%{_libexecdir}/pdb-fixer/openmm_plugins/libOpenMMCPU.so

%check
export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset PYTHONHOME

export OPENMM_PLUGIN_DIR="%{buildroot}%{_libexecdir}/pdb-fixer/openmm_plugins"

%{buildroot}%{_libexecdir}/pdb-fixer/pdb-fixer --help
%{buildroot}%{_bindir}/pdb-fixer --help

%files
%{_bindir}/pdb-fixer
%{_libexecdir}/pdb-fixer/

%changelog
* Tue Jul 14 2026 Benjamin Gallois - 1.0.0-1
- Initial RPM package
- Bundle Python 3.11, OpenMM, and pdbfixer-neoralab
- Bundle OpenMM runtime plugins, including the CPU platform
