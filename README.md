# Hugging Face Model Downloader

A simple utility for downloading and managing Hugging Face models on an NFS share. This tool helps you download models from Hugging Face and store them in a centralized NFS location for easy access across your network.

## Project Structure

- `mount.sh` - Script to mount the NFS share and set up permissions
- `download.py` - Python script to download models from Hugging Face

## Prerequisites

- Linux system with NFS client support
- Python 3.x
- Access to an NFS server
- sudo privileges for mounting NFS share

## Setup Instructions

### 1. Configure NFS Share

Edit `mount.sh` to set your NFS server details:
```bash
NFS_SERVER="192.168.1.100"  # Change to your NFS server IP
NFS_SHARE="/path/to/share"  # Change to your NFS share path
MOUNT_POINT="/mnt/ai_models"
```

### 2. Create Python Virtual Environment

```bash
# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install --upgrade pip
pip install --upgrade huggingface-hub
```

### 3. Mount NFS Share

```bash
# Make the script executable
chmod +x mount.sh

# Run the mount script
sudo ./mount.sh
```

## Usage

### Downloading Models

With the virtual environment activated, use the download script:

```bash
python3 download.py <repository-id>
```

Examples:
```bash
# Download Qwen model
python3 download.py Qwen/Qwen3-Embedding-4B

# Download GGUF model
python3 download.py unsloth/sqwen3_GGUF

# Download other models
python3 download.py cpatonn/Qwen3-VL-8B-Instruct-AWQ-8bit
```

The models will be downloaded to your NFS share in a directory structure matching the repository name:
```
/mnt/ai_models/
├── Qwen/
│   └── Qwen3-Embedding-4B/
├── unsloth/
│   └── sqwen3_GGUF/
└── ...
```

## Features

- **Automatic Directory Structure**: Creates nested directories based on repository names
- **Resume Support**: Can resume interrupted downloads
- **Smart Downloads**: Only downloads new or changed files
- **NFS Integration**: Centralized storage accessible across your network
- **Permission Management**: Handles NFS mount permissions automatically

## Troubleshooting

### NFS Mount Issues

If you encounter permission issues:
1. Ensure the NFS server allows write access
2. Check if the NFS share is properly mounted:
   ```bash
   mount | grep ai_models
   ```
3. Verify permissions:
   ```bash
   ls -la /mnt/ai_models
   ```

### Download Issues

If downloads fail:
1. Ensure your virtual environment is activated
2. Check internet connection
3. Verify the repository ID is correct
4. Ensure sufficient disk space on NFS share

## Maintenance

- Keep huggingface-hub updated:
  ```bash
  pip install --upgrade huggingface-hub
  ```
- Regularly check NFS mount status
- Monitor available disk space on NFS share

## Unmounting

To unmount the NFS share:
```bash
sudo umount /mnt/ai_models
```

## Licence
MIT
