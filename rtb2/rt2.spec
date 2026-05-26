%global debug_package %{nil}

Name:           rtb2
Version:        1.0.0
Release:        1%{?dist}
Summary:        RTB2 - Rotation-Translation Block normal mode analysis tools

License:        Proprietary
URL:            https://github.com/MDSPACE-toolkit/rtb2

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  blas-devel
BuildRequires:  arpack-devel
BuildRequires:  flexiblas-devel

%description
RTB2 provides tools for rotation-translation block normal mode analysis.
This package installs the RTB2 binaries and the makebloc.pl helper script.

%prep
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
ssh-keyscan -H github.com > "$HOME/.ssh/known_hosts"
chmod 600 "$HOME/.ssh/known_hosts"
GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/root/.ssh/known_hosts" \
git clone git@github.com:MDSPACE-toolkit/rtb2.git rtb2-1.0.0

%build
cd rtb2-1.0.0/src
mkdir -p build
cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix}

make

%install
mkdir -p %{buildroot}%{_bindir}

install -m 0755 rtb2-1.0.0/src/build/rtb2 %{buildroot}%{_bindir}/rtb2
install -m 0755 rtb2-1.0.0/scripts/makebloc.pl %{buildroot}%{_bindir}/makebloc.pl

%files
%{_bindir}/rtb2
%{_bindir}/makebloc.pl

%changelog
* Tue May 26 2026 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr> - 1.0.0-1
- Initial package build for RTB2.
