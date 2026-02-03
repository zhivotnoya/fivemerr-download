#!/usr/bin/env python3
"""
Download images from URLs listed in a CSV file.
Reads URLs from the 'file_url' column and saves images to the current directory.
"""

import csv
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_filename_from_url(url, index):
    """Extract filename from URL or generate one."""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    # If no filename or no extension, generate one
    if not filename or '.' not in filename:
        # Try to get extension from content-type later
        filename = f"image_{index:04d}"

    return filename

def download_image(session, url, output_dir, index):
    """Download a single image from URL."""
    try:
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()

        # Get filename
        filename = get_filename_from_url(url, index)

        # If no extension, try to infer from content-type
        if '.' not in filename:
            content_type = response.headers.get('content-type', '')
            ext_map = {
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'image/gif': '.gif',
                'image/webp': '.webp',
                'image/bmp': '.bmp',
            }
            ext = ext_map.get(content_type, '.jpg')
            filename += ext

        filepath = output_dir / filename

        # Handle duplicate filenames
        counter = 1
        original_filepath = filepath
        while filepath.exists():
            stem = original_filepath.stem
            suffix = original_filepath.suffix
            filepath = output_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        # Download and save
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True, filename

    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_images.py <csv_file>")
        print("Example: python download_images.py images.csv")
        sys.exit(1)

    csv_file = sys.argv[1]

    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        sys.exit(1)

    # Create output directory
    output_dir = Path("downloaded_images")
    output_dir.mkdir(exist_ok=True)

    print(f"Reading URLs from: {csv_file}")
    print(f"Downloading images to: {output_dir}/")
    print("-" * 60)

    session = create_session()

    successful = 0
    failed = 0
    failed_urls = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check if file_url column exists
            if 'file_url' not in reader.fieldnames:
                print(f"Error: CSV file must have a 'file_url' column.")
                print(f"Found columns: {', '.join(reader.fieldnames)}")
                sys.exit(1)

            for index, row in enumerate(reader, start=1):
                url = row.get('file_url', '').strip()

                if not url:
                    print(f"Row {index}: Skipping empty URL")
                    continue

                print(f"[{index}] Downloading: {url[:60]}...")
                success, result = download_image(session, url, output_dir, index)

                if success:
                    print(f"     ✓ Saved as: {result}")
                    successful += 1
                else:
                    print(f"     ✗ Failed: {result}")
                    failed += 1
                    failed_urls.append((url, result))

    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
    except Exception as e:
        print(f"\nError reading CSV file: {e}")
        sys.exit(1)

    # Summary
    print("-" * 60)
    print(f"Download complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if failed_urls:
        print("\nFailed downloads:")
        for url, error in failed_urls:
            print(f"  - {url}")
            print(f"    Error: {error}")

if __name__ == "__main__":
    main()
