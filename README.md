# Fiverr Image Downloader & Utilities

> **Note:** This project was created to preserve images from Fiverr before the service shutdown on March 5, 2026. These scripts can be adapted for other CSV-based image downloading needs.

A collection of Python utilities for downloading images from CSV exports and processing them.

## 🚀 Features

- **Download images** from CSV files containing URLs
- **Convert WebP images** to PNG format
- **Automatically detect and fix** `.undefined` file extensions

## 📋 Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/fivemerr-download.git
cd fivemerr-download
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### 1. Download Images from CSV (`fivemerr-dump.py`)

Downloads images from URLs listed in a CSV file with a `file_url` column.

```bash
./fivemerr-dump.py your_file.csv
```

**Features:**
- Automatic retry logic for failed downloads
- Smart filename generation from URLs
- Duplicate filename handling
- Progress tracking with detailed output
- Downloaded images saved to `downloaded_images/` directory

**Example CSV format:**
```csv
file_url
https://example.com/image1.jpg
https://example.com/image2.png
```

### 2. Convert WebP to PNG (`img-convert.py`)

Converts all `.webp` images in a directory to `.png` format.

```bash
# Convert in current directory
./img-convert.py

# Convert in specific directory
./img-convert.py downloaded_images

# Convert and delete originals
./img-convert.py downloaded_images --delete
```

**Options:**
- `-d, --delete` - Delete original WebP files after conversion
- `-h, --help` - Show help message

### 3. Fix Undefined Extensions (`renund.py`)

Detects actual image types of `.undefined` files using file signatures and renames them with correct extensions.

```bash
# Rename files in current directory
./renund.py

# Rename files in specific directory
./renund.py downloaded_images

# Dry run (preview changes without renaming)
./renund.py --dry-run
```

**Options:**
- `-n, --dry-run` - Preview changes without actually renaming
- `-h, --help` - Show help message

**Supported formats:**
- JPEG/JPG
- PNG
- GIF
- WebP
- BMP
- ICO
- TIFF

## 🔄 Typical Workflow

```bash
# 1. Download images from CSV
./fivemerr-dump.py my_images.csv

# 2. Fix any .undefined files
./renund.py downloaded_images

# 3. Convert WebP to PNG (optional)
./img-convert.py downloaded_images --delete
```

## 📁 Project Structure

```
fivemerr-download/
├── fivemerr-dump.py          # CSV image downloader
├── img-convert.py            # WebP to PNG converter
├── renund.py                 # Undefined file renamer
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── downloaded_images/        # Default output directory (created automatically)
```

## 🛠️ Technical Details

### Error Handling
All scripts include comprehensive error handling:
- Network failures with automatic retry
- File system errors
- Malformed URLs
- Invalid file formats

### File Naming
- Automatic duplicate detection
- Sequential numbering for conflicts
- Preservation of original filenames when possible

### Performance
- Streaming downloads for large files
- Chunked file processing
- Efficient magic number detection

## 🤝 Contributing

Feel free to open issues or submit pull requests if you find bugs or have improvements to suggest.

## 📜 License

MIT License - feel free to use and modify these scripts for your own needs.

## ⚠️ Disclaimer

This project was created to help users preserve their data from Fiverr before its shutdown. Always respect website terms of service and rate limits when downloading content.

## 🙏 Acknowledgments

Created with assistance from GitHub Copilot to help preserve user data before the Fiverr service shutdown in March 2026.
