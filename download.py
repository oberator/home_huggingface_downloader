from huggingface_hub import snapshot_download
import os
import argparse
import hashlib

# === VARIABLES ===
# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Download a model from Hugging Face Hub",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python3 download.py microsoft/DialoGPT-medium /path/to/download
  python3 download.py microsoft/DialoGPT-medium /path/to/download --exclude=*.safetensors,original/*
  python3 download.py meta-llama/Llama-2-7b-hf /models/llama2 --exclude=*.bin,*.pt
    """
)
parser.add_argument("repository_id", help="Hugging Face repository ID (e.g., microsoft/DialoGPT-medium)")
parser.add_argument("download_path", help="Local directory path where the model will be downloaded")
parser.add_argument("--exclude", help="Comma-separated list of patterns to exclude (e.g., *.safetensors,original/*)", default="")

args = parser.parse_args()

download_url = args.repository_id
download_path = args.download_path

# Parse the comma-separated exclude patterns
custom_excludes = []
if args.exclude:
    custom_excludes = [pattern.strip() for pattern in args.exclude.split(",")]

# Make sure the local directory exists
os.makedirs(download_path, exist_ok=True)

# Combine default ignores with user provided ignores
base_ignores = ["*.lock"]
final_ignore_patterns = base_ignores + custom_excludes

print(f"Downloading model: {download_url}")
print(f"Destination: {download_path}")

if custom_excludes:
    print(f"Excluding patterns: {', '.join(custom_excludes)}")

# Download the model
snapshot_download(
    repo_id=download_url,
    local_dir=download_path,
    ignore_patterns=final_ignore_patterns, # Updated to use the combined list
    force_download=False,  # Only download if files don't exist or are different
)

print(f"Model downloaded to: {download_path}")

# Calculate SHA256 hash of the downloaded directory
def calculate_directory_hash(directory_path):
    """Calculate SHA256 hash of all files in a directory."""
    sha256_hash = hashlib.sha256()
    
    # Get all files in directory recursively
    for root, dirs, files in os.walk(directory_path):
        # Sort files for consistent hash
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            # Skip .lock files and .sha256 files
            if filename.endswith('.lock') or filename.endswith('.sha256'):
                continue
            
            try:
                with open(filepath, 'rb') as f:
                    # Read file in chunks to handle large files
                    for chunk in iter(lambda: f.read(4096), b''):
                        sha256_hash.update(chunk)
            except (IOError, OSError) as e:
                print(f"Warning: Could not read {filepath}: {e}")
    
    return sha256_hash.hexdigest()

# Calculate and display the hash
print("Calculating SHA256 hash of downloaded files...")
directory_hash = calculate_directory_hash(download_path)
print(f"SHA256 hash: {directory_hash}")

# Store the hash in a .sha256 file within the download directory
hash_file_path = os.path.join(download_path, ".sha256")
with open(hash_file_path, 'w') as f:
    f.write(directory_hash + '\n')
print(f"SHA256 hash stored in: {hash_file_path}")
