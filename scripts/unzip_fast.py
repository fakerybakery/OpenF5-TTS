#!/usr/bin/env python3
import os
import subprocess
import concurrent.futures
import argparse
from pathlib import Path
from tqdm import tqdm

def extract_tar(tar_path, output_dir=None):
    """Extract a tar file using system tar command and delete it if successful."""
    try:
        # Get the base name without extension
        basename = os.path.basename(tar_path)
        name_without_ext = os.path.splitext(basename)[0]

        # Use provided output dir or create in same location as tar
        if output_dir:
            extract_dir = os.path.join(output_dir, name_without_ext)
        else:
            extract_dir = os.path.join(os.path.dirname(tar_path), name_without_ext)

        # Create the directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)

        # Use system tar command with minimal output
        cmd = ["tar", "-xf", tar_path, "-C", extract_dir]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)

        # Remove tar file after successful extraction
        os.remove(tar_path)

        return True, tar_path
    except subprocess.CalledProcessError as e:
        return False, f"{tar_path}: {e.stderr}"
    except Exception as e:
        return False, f"{tar_path}: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Extract multiple tar files in parallel with maximum efficiency")
    parser.add_argument("directory", help="Directory containing tar files")
    parser.add_argument("-o", "--output", help="Output directory (default: same as tar files)")
    parser.add_argument("-p", "--processes", type=int, default=os.cpu_count(),
                        help=f"Number of processes to use (default: {os.cpu_count()})")
    args = parser.parse_args()

    input_dir = Path(args.directory)
    output_dir = Path(args.output) if args.output else None

    # Verify tar command is available
    if subprocess.call(["tar", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("Error: 'tar' command not found. Please ensure tar is installed.")
        return

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: {input_dir} is not a valid directory")
        return

    if output_dir and not output_dir.exists():
        os.makedirs(output_dir, exist_ok=True)

    # Get all tar files in the directory
    tar_files = [str(f) for f in input_dir.glob("*.tar")]

    if not tar_files:
        print("No .tar files found in the specified directory.")
        return

    print(f"Found {len(tar_files)} tar files to extract")

    # Use ProcessPoolExecutor for true parallelism
    with tqdm(total=len(tar_files), desc="Overall Progress", unit="file") as pbar:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.processes) as executor:
            futures = {executor.submit(extract_tar, tar_path, output_dir): tar_path 
                      for tar_path in tar_files}

            for future in concurrent.futures.as_completed(futures):
                success, result = future.result()
                if not success:
                    print(f"Error extracting {result}")
                pbar.update(1)

    print("Extraction complete!")

if __name__ == "__main__":
    main()
