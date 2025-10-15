from huggingface_hub import snapshot_download
import os
import sys

# === VARIABLES ===
# Check if repository URL is provided as command line argument
if len(sys.argv) < 2:
    print("Usage: python3 download.py <repository_id>")
    print("Example: python3 download.py microsoft/DialoGPT-medium")
    sys.exit(1)

download_url = sys.argv[1]
nfs_root = "/mnt/ai_models"

# Construct the download path dynamically from the model name
download_path = os.path.join(nfs_root, download_url.replace("/", os.sep))

# Make sure the local directory exists
os.makedirs(download_path, exist_ok=True)

print(f"Downloading model: {download_url}")
print(f"Destination: {download_path}")

# Download the model
snapshot_download(
    repo_id=download_url,
    local_dir=download_path,
    ignore_patterns=["*.lock"],  # optional, can avoid lock files
    force_download=False,  # Only download if files don't exist or are different
)

print(f"Model downloaded to: {download_path}")
