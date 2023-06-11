#!/bin/bash

VYOS_VERSION=${VERSION:=latest}

# Create temp work directory
[ -d "vyos" ] || mkdir -p vyos
pushd vyos

# Download ISO
iso_file=vyos-$VYOS_VERSION-amd64.iso
[ -f $iso_file ] || wget https://s3-us.vyos.io/rolling/current/$iso_file

# Create temp rootfs directory for mount
[ -d rootfs ] || mkdir -p rootfs

# Mount iso to rootfs
sudo umount rootfs
sudo mount -o loop $iso_file rootfs

if (! command -v unsquashfs); then
    echo "unsquashfs not found, exiting..."
    exit 1
fi
# Create temp unsquash directory
[ -d unsquashfs ] || mkdir -p unsquashfs

# Unsquash filesystem from vyos
sudo unsquashfs -f -d unsquashfs/ rootfs/live/filesystem.squashfs

# Create archive from unsquashed filesystem and import to docker
sudo tar -C unsquashfs -c . | docker import - ghcr.io/routedbits/vyos:$VYOS_VERSION

# Cleanup
sudo umount rootfs
popd
sudo rm -rf vyos

# Push image to GitHub registry
#docker push ghcr.io/routedbits/vyos:$VYOS_VERSION
