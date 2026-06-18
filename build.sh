#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 <path/to/spec> [output-dir]" >&2
  exit 1
fi

SPEC_PATH="$1"
OUT_DIR="${2:-$PWD}"

if [ ! -f "$SPEC_PATH" ]; then
  echo "ERROR: spec file not found: $SPEC_PATH" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

SPEC_PATH_ABS="$(realpath "$SPEC_PATH")"
OUT_DIR_ABS="$(realpath "$OUT_DIR")"
PROJECT_ROOT="$(realpath "$PWD")"

case "$SPEC_PATH_ABS" in
  "$PROJECT_ROOT"/*)
    ;;
  *)
    echo "ERROR: spec must be inside the current working tree: $PROJECT_ROOT" >&2
    exit 1
    ;;
esac

SPEC_PATH_IN_CONTAINER="/work/${SPEC_PATH_ABS#"$PROJECT_ROOT"/}"
SPEC_BASENAME="$(basename "$SPEC_PATH_ABS")"
SPEC_DIR_IN_CONTAINER="$(dirname "$SPEC_PATH_IN_CONTAINER")"

docker run --rm \
  -v "$PROJECT_ROOT:/work" \
  -v "$OUT_DIR_ABS:/out" \
  -w /work \
  -e SPEC_IN_CONTAINER="$SPEC_PATH_IN_CONTAINER" \
  -e SPEC_BASENAME="$SPEC_BASENAME" \
  -e SPEC_DIR_IN_CONTAINER="$SPEC_DIR_IN_CONTAINER" \
  almalinux:10 \
  bash -lc '
    set -euo pipefail

    dnf -y install epel-release
    dnf config-manager --set-enabled crb

    dnf -y install \
      dnf-plugins-core \
      rpm-build \
      rpmdevtools \
      redhat-rpm-config \
      wget \
      curl-minimal \
      git \
      which \
      tar \
      gzip \
      bzip2 \
      xz \
      make \
      gcc \
      gcc-c++ \
      patch

    rpmdev-setuptree

    cp \
      "$SPEC_IN_CONTAINER" \
      "/root/rpmbuild/SPECS/$SPEC_BASENAME"

    find "$SPEC_DIR_IN_CONTAINER" \
      -maxdepth 1 \
      -type f \
      ! -name "*.spec" \
      -exec cp -v {} /root/rpmbuild/SOURCES/ \; \
      || true

    SPEC_FILE="/root/rpmbuild/SPECS/$SPEC_BASENAME"

    spectool \
      -g \
      -R \
      --define "_sourcedir /root/rpmbuild/SOURCES" \
      "$SPEC_FILE"

    dnf -y \
      builddep \
      "$SPEC_FILE"

    rpmbuild -ba \
      --define "_topdir /root/rpmbuild" \
      --define "_sourcedir /root/rpmbuild/SOURCES" \
      --define "_specdir /root/rpmbuild/SPECS" \
      --define "_builddir /root/rpmbuild/BUILD" \
      --define "_srcrpmdir /root/rpmbuild/SRPMS" \
      --define "_rpmdir /root/rpmbuild/RPMS" \
      "$SPEC_FILE"

    cp -v /root/rpmbuild/RPMS/*/*.rpm /out/
    cp -v /root/rpmbuild/SRPMS/*.src.rpm /out/
  '
