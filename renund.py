#!/usr/bin/env python3
"""
Detect the actual image type of .undefined files and rename them with the correct extension.
Uses file signatures (magic numbers) to identify the true file type.
"""

import sys
import os
from pathlib import Path

# File signatures (magic numbers) for common image formats
IMAGE_SIGNATURES = {
    b'\xFF\xD8\xFF': '.jpg',           # JPEG
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': '.png',  # PNG
    b'GIF87a': '.gif',                  # GIF 87a
    b'GIF89a': '.gif',                  # GIF 89a
    b'RIFF': '.webp',                   # WebP (needs additional check)
    b'BM': '.bmp',                      # BMP
    b'\x00\x00\x01\x00': '.ico',       # ICO
    b'\x00\x00\x02\x00': '.cur',       # CUR
    b'II\x2A\x00': '.tif',             # TIFF (little-endian)
    b'MM\x00\x2A': '.tif',             # TIFF (big-endian)
}

def detect_image_type(file_path):
    """Detect the image type by reading file signature."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)  # Read first 12 bytes

        # Check for exact matches first
        for signature, extension in IMAGE_SIGNATURES.items():
            if header.startswith(signature):
                # Special case for WebP - need to verify
                if extension == '.webp':
                    if b'WEBP' in header:
                        return extension
                else:
                    return extension

        return None

    except Exception as e:
        return None

def rename_undefined_file(file_path, dry_run=False):
    """Rename a .undefined file to its actual type."""
    try:
        # Detect the actual image type
        actual_extension = detect_image_type(file_path)

        if actual_extension is None:
            return False, f"Could not detect image type: {file_path.name}"

        # Create new filename
        new_path = file_path.with_suffix(actual_extension)

        # Handle duplicates
        counter = 1
        original_new_path = new_path
        while new_path.exists():
            stem = original_new_path.stem
            suffix = original_new_path.suffix
            new_path = file_path.parent / f"{stem}_{counter}{suffix}"
            counter += 1

        if dry_run:
            return True, f"Would rename: {file_path.name} → {new_path.name}"
        else:
            # Rename the file
            file_path.rename(new_path)
            return True, f"Renamed: {file_path.name} → {new_path.name}"

    except Exception as e:
        return False, f"Failed to rename {file_path.name}: {str(e)}"

def main():
    # Parse arguments
    dry_run = False
    directory = "."

    if len(sys.argv) > 1:
        if sys.argv[1] in ['--dry-run', '-n']:
            dry_run = True
            if len(sys.argv) > 2:
                directory = sys.argv[2]
        else:
            directory = sys.argv[1]
            if len(sys.argv) > 2 and sys.argv[2] in ['--dry-run', '-n']:
                dry_run = True

    # Convert to Path object
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)

    # Find all .undefined files
    undefined_files = list(dir_path.glob('*.undefined'))

    if not undefined_files:
        print(f"No .undefined files found in '{directory}'")
        sys.exit(0)

    print(f"Found {len(undefined_files)} .undefined file(s) in '{directory}'")
    if dry_run:
        print("DRY RUN MODE - No files will be renamed")
    print("-" * 60)

    successful = 0
    failed = 0
    detected_types = {}

    for undefined_file in undefined_files:
        success, message = rename_undefined_file(undefined_file, dry_run)

        if success:
            print(f"✓ {message}")
            successful += 1

            # Track detected types
            actual_type = detect_image_type(undefined_file)
            if actual_type:
                detected_types[actual_type] = detected_types.get(actual_type, 0) + 1
        else:
            print(f"✗ {message}")
            failed += 1

    # Summary
    print("-" * 60)
    print(f"Processing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if detected_types:
        print("\nDetected file types:")
        for ext, count in sorted(detected_types.items()):
            print(f"  {ext}: {count} file(s)")

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print("Usage: python rename_undefined_images.py [directory] [--dry-run|-n]")
        print()
        print("Detect actual image types of .undefined files and rename them")
        print()
        print("Arguments:")
        print("  directory          Directory to search (default: current directory)")
        print("  --dry-run, -n      Show what would be renamed without actually renaming")
        print()
        print("Examples:")
        print("  python rename_undefined_images.py")
        print("  python rename_undefined_images.py downloaded_images")
        print("  python rename_undefined_images.py --dry-run")
        print("  python rename_undefined_images.py downloaded_images --dry-run")
        sys.exit(0)

    main()
