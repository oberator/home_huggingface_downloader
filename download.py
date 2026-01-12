from huggingface_hub import snapshot_download
import os
import argparse

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
