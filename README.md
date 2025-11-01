# MDSPACE External RPMs

This repository provides RPM packages for external dependencies required by **MDSPACE**. These RPM packages are intended to simplify the installation of required libraries and tools needed to run the MDSPACE software.

---

## Requirements

Before building and installing the external dependencies, ensure that the following development tools and libraries are available on your system:

* **gcc** (GNU Compiler Collection)
* **make** (build tool)
* **rpm-build** (RPM packaging tool)
* **rpmdevtools** (RPM development tools)

---

## Installing the RPMs

These external dependencies are packaged as RPM files, which can be installed on a system running **Red Hat-based distributions** (such as RHEL or CentOS). To install them, follow these steps:

### Step 1: Download or Clone the Repository

You can either clone this repository or directly download the RPMs from the latest release.

```bash
git clone https://https://github.com/MDSPACE-toolkit/mdspace-external-rpms
cd mdspace-external-rpms
```

### Step 2: Build the RPM Packages (Optional)

If you need to build the RPM packages from source, use the following steps:

1. Ensure that **rpm-build** and **rpmdevtools** are installed:

   ```bash
   sudo dnf install rpm-build rpmdevtools
   ```

2. Build the RPMs from the `spec` files:

   ```bash
   rpmbuild -ba <package_name>/<package_name>.spec
   ```

   This will create the RPM packages in the `~/rpmbuild/RPMS/` directory.

### Step 3: Install the RPM Packages

Once the RPM packages are built or downloaded, install them with `dnf`:

```bash
sudo dnf install ~/rpmbuild/RPMS/package.rpm
```

---
