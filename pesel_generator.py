#!/usr/bin/env python3
"""Module for generating valid Polish PESEL numbers for a given range of years."""

import argparse
import os
from datetime import datetime, timedelta
from typing import List, Optional


def calculate_check_digit(pesel_base: str) -> int:
    """Calculate the check digit for a PESEL number."""
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    total = 0
    for i in range(10):
        total += int(pesel_base[i]) * weights[i]
    check_digit = (10 - (total % 10)) % 10
    return check_digit


def generate_sequential_and_sex_digits(sequential_number: int, is_male: bool) -> str:
    """Generate digits 7-10 of PESEL number.

    Args:
        sequential_number: Number from 0 to 9999
        is_male: True for male, False for female

    Returns:
        String containing digits 7-10, where the number is odd for males and even for females
    """
    # Ensure sequential number is within range
    sequential_number = max(0, min(9999, sequential_number))

    # If the sequential number doesn't match the required sex (odd/even),
    # adjust it by adding 1 or subtracting 1
    is_odd = sequential_number % 2 == 1
    if is_male != is_odd:
        if is_male:
            sequential_number += 1  # Make it odd for male
        else:
            sequential_number -= 1  # Make it even for female

    # Format sequential number with leading zeros (4 digits)
    return f"{sequential_number:04d}"


def format_date_for_pesel(date: datetime) -> str:
    """Format date for PESEL number.

    Month number is modified based on century:
    - 1800-1899: add 80 to month
    - 1900-1999: no modification (month 01-12)
    - 2000-2099: add 20 to month
    - 2100-2199: add 40 to month
    - 2200-2299: add 60 to month

    For example:
    - 01.01.1800 -> 8001 (month 81)
    - 01.01.1900 -> 0001 (month 01)
    - 01.01.2000 -> 0001 (month 01)
    - 01.01.2020 -> 2101 (month 21)
    - 01.01.2100 -> 0041 (month 41)
    """
    year = date.year
    month = date.month
    day = date.day

    # Add century-specific offset to month
    if 1800 <= year <= 1899:
        month += 80
    elif 2000 <= year <= 2099:
        month += 20
    elif 2100 <= year <= 2199:
        month += 40
    elif 2200 <= year <= 2299:
        month += 60
    # For 1900-1999, no modification needed

    return f"{year % 100:02d}{month:02d}{day:02d}"


def generate_pesel_for_date(date: datetime, sequential_number: int, is_male: bool) -> str:
    """Generate a valid PESEL number for a given date."""
    # Format date as YYMMDD with proper month encoding for XXI century
    date_str = format_date_for_pesel(date)

    # Generate sequential and sex digits
    seq_sex_digits = generate_sequential_and_sex_digits(
        sequential_number, is_male)

    # Combine date and sequential/sex digits
    pesel_base = date_str + seq_sex_digits

    # Calculate check digit
    check_digit = calculate_check_digit(pesel_base)

    # Return complete PESEL
    return pesel_base + str(check_digit)


def generate_pesels_for_year_range(
    start_year: int,
    end_year: int,
    is_male: Optional[bool] = None
) -> List[str]:
    """Generate all possible PESEL numbers for a given year range.

    Args:
        start_year: Starting year (YYYY)
        end_year: Ending year (YYYY)
        is_male: If True, generate only male PESELs. If False, generate only female
                PESELs. If None, generate both male and female PESELs.
    """
    pesels = []
    current_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    # Calculate total days for progress tracking
    total_days = (end_date - current_date).days + 1
    days_processed = 0
    last_progress = -1  # Track last printed progress percentage
    bar_width = 50  # Width of the progress bar in characters

    while current_date <= end_date:
        # Generate PESELs for all sequential numbers
        for seq_num in range(10000):
            # If sex is specified, only generate for that sex
            if is_male is not None:
                if (is_male and seq_num % 2 == 1) or (not is_male and seq_num % 2 == 0):
                    pesels.append(generate_pesel_for_date(
                        current_date, seq_num, is_male))
            else:
                # Generate for both sexes
                pesels.append(generate_pesel_for_date(
                    current_date, seq_num, seq_num % 2 == 1))

        days_processed += 1
        current_progress = int((days_processed / total_days) * 100)

        # Only update progress bar when the percentage changes
        if current_progress != last_progress:
            filled_length = int(bar_width * days_processed // total_days)
            progress_bar = '=' * filled_length + \
                '-' * (bar_width - filled_length)
            print(f"\rProgress: [{progress_bar}] {current_progress}%",
                  end="", flush=True)
            last_progress = current_progress

        current_date += timedelta(days=1)

    print()  # New line after progress
    return pesels


def main():
    """Parse command line arguments and generate PESEL numbers based on the provided parameters."""
    parser = argparse.ArgumentParser(
        description='Generate PESEL numbers for a given year range')
    parser.add_argument('start_year', type=int, help='Starting year (YYYY)')
    parser.add_argument('end_year', type=int, nargs='?', default=None,
                        help='Ending year (YYYY). If not provided, '
                             'generates PESELs for start_year only.')
    parser.add_argument('--output', '-o', type=str,
                        help='Output file path (optional)')
    parser.add_argument(
        '--sex', '-s', choices=['male', 'female'], help='Generate PESELs for specific sex only')

    args = parser.parse_args()

    # If end_year is not provided, use start_year
    if args.end_year is None:
        args.end_year = args.start_year

    if args.start_year < 1800 or args.end_year > 2299:
        print("Error: Year range must be between 1800 and 2299")
        return

    if args.start_year > args.end_year:
        print("Error: Start year must be less than or equal to end year")
        return

    # Convert sex argument to boolean
    is_male: Optional[bool] = None
    if args.sex == 'male':
        is_male = True
    elif args.sex == 'female':
        is_male = False

    print(
        f"Generating PESEL numbers for years {args.start_year}-{args.end_year}...")
    if is_male is not None:
        print(f"Generating only {'male' if is_male else 'female'} PESELs")

    pesels = generate_pesels_for_year_range(
        args.start_year, args.end_year, is_male)

    if args.output:
        if os.path.exists(args.output):
            response = input(
                f"File {args.output} already exists. Overwrite? [y/N] ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return
        with open(args.output, 'w', encoding='utf-8') as f:
            for pesel in pesels:
                f.write(f"{pesel}\n")
        print(
            f"Generated {len(pesels)} PESEL numbers and saved to {args.output}")
    else:
        for pesel in pesels:
            print(pesel)
        print(f"\nGenerated {len(pesels)} PESEL numbers")


if __name__ == "__main__":
    main()
