#!/usr/bin/env python3
"""Wrapper script to generate PESEL numbers for a range of years with separate files."""

import os
import subprocess
from typing import Tuple


def create_output_directory() -> str:
    """Create output directory if it doesn't exist."""
    output_dir = "generated_pesels"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def generate_pesels_for_year(year: int, output_dir: str, sex: str) -> Tuple[str, bool]:
    """Generate PESELs for a specific year and sex.

    Returns:
        Tuple of (output filename, success boolean)
    """
    output_file = os.path.join(output_dir, f"{year}_{sex}.txt")

    # Skip if file already exists
    if os.path.exists(output_file):
        print(f"File {output_file} already exists, skipping...")
        return output_file, False

    print(f"Generating {sex} PESELs for year {year}...")

    # Run pesel_generator.py with appropriate arguments
    try:
        subprocess.run(
            [
                "python3",
                "pesel_generator.py",
                str(year),
                "--sex",
                sex,
                "--output",
                output_file
            ],
            check=True
        )
        return output_file, True
    except subprocess.CalledProcessError as e:
        print(f"Error generating PESELs for year {year} and sex {sex}: {e}")
        return output_file, False


def main():
    """Generate PESELs for years 1950-2030 with separate files for each year and sex."""
    start_year = 1950
    end_year = 2030

    # Create output directory
    output_dir = create_output_directory()
    print(f"Storing generated files in: {output_dir}")

    # Track statistics
    total_files = 0
    total_size = 0

    # Generate PESELs for each year and sex
    for year in range(start_year, end_year + 1):
        for sex in ['male', 'female']:
            output_file, success = generate_pesels_for_year(
                year, output_dir, sex)

            if success:
                file_size = os.path.getsize(output_file)
                total_files += 1
                total_size += file_size
                print(
                    f"Generated {output_file} ({file_size / (1024*1024):.1f} MB)")

    # Print summary
    print("\nGeneration complete!")
    print(f"Total files generated: {total_files}")
    print(f"Total size: {total_size / (1024*1024*1024):.1f} GB")


if __name__ == "__main__":
    main()
