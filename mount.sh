#!/bin/bash

# === VARIABLES ===
NFS_SERVER="10.10.0.30"
NFS_SHARE="/volume1/ai_models"
MOUNT_POINT="/mnt/ai_models"
CURRENT_USER="$USER"
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)

# === STEP 1: Mount NFS share ===
if mountpoint -q "$MOUNT_POINT"; then
    echo "Unmounting existing NFS share..."
    sudo umount -f "$MOUNT_POINT"
fi

echo "Mounting NFS share..."
# Create mount point with correct permissions
sudo mkdir -p "$MOUNT_POINT"
sudo chmod 777 "$MOUNT_POINT"

# Mount with specific user permissions
sudo mount -t nfs -o rw,nfsvers=3,nolock "$NFS_SERVER:$NFS_SHARE" "$MOUNT_POINT"
if [ $? -ne 0 ]; then
    echo "Failed to mount NFS share. Exiting."
    exit 1
fi

# Set liberal permissions for the mount point and its contents
echo "Setting permissions..."
sudo chmod -R 777 "$MOUNT_POINT"
echo "Mounted NFS share with write permissions"

# === STEP 2: Install huggingface-hub ===
echo "Installing huggingface-hub..."
pip install --upgrade huggingface-hub
