#!/usr/bin/env python3
"""
Convert all .webp images in a directory to .png format.
Can optionally delete the original .webp files after conversion.
"""

import sys
import os
from pathlib import Path
from PIL import Image

def convert_webp_to_png(webp_path, delete_original=False):
    """Convert a single .webp file to .png"""
    try:
        # Open the webp image
        img = Image.open(webp_path)

        # Create the output filename
        png_path = webp_path.with_suffix('.png')

        # Convert and save as PNG
        img.save(png_path, 'PNG')

        # Optionally delete the original
        if delete_original:
            webp_path.unlink()
            return True, f"Converted and deleted: {webp_path.name}"
        else:
            return True, f"Converted: {webp_path.name} → {png_path.name}"

    except Exception as e:
        return False, f"Failed to convert {webp_path.name}: {str(e)}"

def main():
    # Parse arguments
    delete_original = False
    directory = "."

    if len(sys.argv) > 1:
        if sys.argv[1] in ['-d', '--delete']:
            delete_original = True
            if len(sys.argv) > 2:
                directory = sys.argv[2]
        else:
            directory = sys.argv[1]
            if len(sys.argv) > 2 and sys.argv[2] in ['-d', '--delete']:
                delete_original = True

    # Convert to Path object
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: Directory '{directory}' not found.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)

    # Find all .webp files
    webp_files = list(dir_path.glob('*.webp'))

    if not webp_files:
        print(f"No .webp files found in '{directory}'")
        sys.exit(0)

    print(f"Found {len(webp_files)} .webp file(s) in '{directory}'")
    if delete_original:
        print("Original .webp files will be DELETED after conversion")
    print("-" * 60)

    successful = 0
    failed = 0

    for webp_file in webp_files:
        success, message = convert_webp_to_png(webp_file, delete_original)

        if success:
            print(f"✓ {message}")
            successful += 1
        else:
            print(f"✗ {message}")
            failed += 1

    # Summary
    print("-" * 60)
    print(f"Conversion complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print("Usage: python convert_webp_to_png.py [directory] [-d|--delete]")
        print()
        print("Convert all .webp images in a directory to .png format")
        print()
        print("Arguments:")
        print("  directory          Directory to search (default: current directory)")
        print("  -d, --delete       Delete original .webp files after conversion")
        print()
        print("Examples:")
        print("  python convert_webp_to_png.py")
        print("  python convert_webp_to_png.py downloaded_images")
        print("  python convert_webp_to_png.py downloaded_images --delete")
        print("  python convert_webp_to_png.py --delete")
        sys.exit(0)

    main()
