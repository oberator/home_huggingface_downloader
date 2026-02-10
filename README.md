# Hugging Face Model Downloader

A Python utility for downloading models from Hugging Face Hub with support for custom download paths, file exclusion patterns, and integrity verification via SHA256 hashing.

## Features

- **Flexible Download Paths**: Specify custom download locations
- **File Exclusion**: Exclude specific file types or patterns during download
- **Integrity Verification**: Automatic SHA256 hash calculation for downloaded files
- **Resume Support**: Resume interrupted downloads
- **Smart Downloads**: Only downloads new or changed files
- **Secure Token Management**: Uses environment variables for authentication

## Prerequisites

- Python 3.x
- Hugging Face account with API token

## Setup Instructions

### 1. Install Dependencies

```bash
# Create a new virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:
```bash
HUGGINGFACE_TOKEN=your_token_here
```

To get your Hugging Face token:
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a new token or copy an existing one
3. Add it to your `.env` file

## Usage

### Basic Download

```bash
python3 download.py <repository_id> <download_path>
```

### Examples

```bash
# Download a model to a specific directory
python3 download.py microsoft/DialoGPT-medium /path/to/download

# Download and exclude certain file types
python3 download.py microsoft/DialoGPT-medium /path/to/download --exclude=*.safetensors,original/*

# Download Llama model, excluding binary files
python3 download.py meta-llama/Llama-2-7b-hf /models/llama2 --exclude=*.bin,*.pt
```

### Command Line Arguments

- `repository_id`: Hugging Face repository ID (e.g., `microsoft/DialoGPT-medium`)
- `download_path`: Local directory path where the model will be downloaded
- `--exclude` (optional): Comma-separated list of patterns to exclude

The script automatically creates a subdirectory structure based on the repository ID:
```
/path/to/download/
└── microsoft/
    └── DialoGPT-medium/
        ├── config.json
        ├── pytorch_model.bin
        ├── .sha256
        └── ...
```

### SHA256 Hash Verification

After each download, the script:
1. Calculates SHA256 hash of all downloaded files
2. Displays the hash in the console
3. Stores the hash in a `.sha256` file within the download directory

This allows you to verify the integrity of downloaded files.

## Project Structure

```
.
├── download.py         # Main download script
├── mount.sh           # NFS mount helper script (optional)
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (not in git)
├── .gitignore        # Git ignore patterns
└── README.md         # This file
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:
1. Verify your token in the `.env` file
2. Ensure the token has the correct permissions
3. Check if the repository requires special access (e.g., gated models)

### Download Issues

- Ensure sufficient disk space at the download location
- Check internet connection
- Verify the repository ID is correct
- For private repositories, ensure your token has access

### Module Import Errors

If you get `ModuleNotFoundError`:
```bash
pip install -r requirements.txt
```

## Advanced Usage

### Using with NFS Shares

If you want to download models to an NFS share:

1. Mount your NFS share (see `mount.sh` for example)
2. Use the mounted path as download location:
   ```bash
   python3 download.py Qwen/Qwen3-Embedding-4B /mnt/ai_models
   ```

## Maintenance

Keep dependencies up to date:
```bash
pip install --upgrade -r requirements.txt
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your Hugging Face token confidential
- The `.gitignore` file is configured to exclude sensitive files

## License

MIT

