%global debug_package %{nil}

Name:           smog2
Version:        2.5
Release:        5%{?dist}
Summary:        SMOG2 - A tool for molecular simulation

License:        GPLv2
URL:            https://smog-server.org/smog2/
Source0:        https://smog-server.org/smog2/code/smog-%{version}.tgz
Source1:        https://www.cpan.org/modules/by-module/XML/XML-Validator-Schema-1.10.tar.gz
Source2:        https://www.cpan.org/authors/id/R/RS/RSAVAGE/Tree-DAG_Node-1.35.tgz

BuildRequires:  gcc
BuildRequires:  gcc-gfortran
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl-devel
BuildRequires:  zlib-devel

Requires:       epel-release
Requires:       perl
Requires:       perl(XML::Parser)
Requires:       perl(XML::SAX)
Requires:       java-21-openjdk

%description
SMOG2 (Structure and Mechanics of Geometries) is a tool for molecular 
simulation and analysis. This package integrates the SMOG2 toolkit into 
the MDSPACE environment.

%prep
%autosetup -n smog-%{version}


tar xf %{SOURCE2}
pushd Tree-DAG_Node-1.35
perl Makefile.PL INSTALLDIRS=vendor
make
popd

tar xf %{SOURCE1}
%build
pushd XML-Validator-Schema-1.10
perl Makefile.PL INSTALLDIRS=vendor
make
popd

echo '#!/bin/bash' > configure
cat configure.smog2 >> configure
chmod +x configure

./configure

mkdir -p bin
cat > bin/smog2 <<'EOF'
#!/bin/bash

SMOG_PATH="/usr/share/smog2"
export PERLLIB="$SMOG_PATH:$PERL5LIB"
export PERL5LIB="$SMOG_PATH:$PERL5LIB"

export perl4smog=/usr/bin/perl
SMOG_PATH="$SMOG_PATH" exec /usr/bin/perl "$SMOG_PATH/smogv2" "$@"
EOF

chmod 755 bin/smog2

cat > bin/smog_adjustPDB <<'EOF'
#!/bin/bash

SMOG_PATH="/usr/share/smog2"
export PERLLIB="$SMOG_PATH:$PERL5LIB"
export PERL5LIB="$SMOG_PATH:$PERL5LIB"

export perl4smog=/usr/bin/perl
SMOG_PATH="$SMOG_PATH" exec /usr/bin/perl "$SMOG_PATH/src/tools/adjustPDB" "$@"
EOF

chmod 755 bin/smog_adjustPDB

# Replace broken absolute symlinks with real directories
for link in SBM_AA SBM_AA+gaussian SBM_calpha SBM_calpha+gaussian; do
    if [ -L "$link" ]; then
        rm -f "$link"
        cp -a "share/templates/$link" "$link"
    fi
done

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/smog2 %{buildroot}%{_bindir}/
install -m 0755 bin/smog_adjustPDB %{buildroot}%{_bindir}/

mkdir -p %{buildroot}/usr/share/smog2
install -m 0644 src/*.pm %{buildroot}/usr/share/smog2/
install -m 0755 src/smogv2 %{buildroot}/usr/share/smog2/
cp -r SBM* %{buildroot}/usr/share/smog2/

mkdir -p %{buildroot}/usr/share/smog2/src/tools
cp -r src/tools/* %{buildroot}/usr/share/smog2/src/tools/
mkdir -p %{buildroot}/usr/share/smog2/share
cp -r share/* %{buildroot}/usr/share/smog2/share/

pushd Tree-DAG_Node-1.35
make DESTDIR=%{buildroot} install
popd

pushd XML-Validator-Schema-1.10
make DESTDIR=%{buildroot} install
popd

rm -f %{buildroot}/usr/lib64/perl5/perllocal.pod
rm -f %{buildroot}/usr/lib64/perl5/vendor_perl/auto/XML/Validator/Schema/.packlist
rm -f %{buildroot}/usr/lib64/perl5/vendor_perl/auto/Tree/DAG_Node/.packlist

%files
%{_bindir}/smog2
%{_bindir}/smog_adjustPDB
/usr/share/smog2
/usr/share/perl5/vendor_perl
/usr/share/man/man3/*.3pm.gz

%changelog
* Sat Nov 01 2025 Benjamin Gallois <benjamin.gallois@sorbonne-universite.fr>
- Initial build for SMOG2 molecular simulation toolkit
