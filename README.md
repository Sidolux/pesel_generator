# PESEL Generator

A Python script for generating valid Polish PESEL numbers for a given year range.

## What is PESEL?

PESEL (Powszechny Elektroniczny System Ewidencji Ludności) is the national identification number used in Poland. It's an 11-digit number that contains encoded information about the person's date of birth and sex.

## Installation

This tool requires Python 3.6 or higher. No additional dependencies are required as it uses only Python standard library.

## Usage

```bash
python3 pesel_generator.py START_YEAR [END_YEAR] [--output FILE] [--sex {male,female}]
```

### Arguments

- `START_YEAR`: Starting year (YYYY)
- `END_YEAR`: Ending year (YYYY). If not provided, generates PESELs for START_YEAR only.
- `--output` or `-o`: Output file path (optional)
- `--sex` or `-s`: Generate PESELs for specific sex only (male or female)

### Examples

Generate PESELs for a single year (2011):

```bash
python3 pesel_generator.py 2011
```

Generate PESELs for a range of years (2011-2015):

```bash
python3 pesel_generator.py 2011 2015
```

Generate male PESELs for 2011 and save to file:

```bash
python3 pesel_generator.py 2011 --sex male --output 2011_male.txt
```

Generate female PESELs for 2011-2015 and save to file:

```bash
python3 pesel_generator.py 2011 2015 --sex female --output 2011_2015_female.txt
```

## Output

The script generates valid PESEL numbers with the following structure:

- First 6 digits: Date of birth (YYMMDD)
- Next 4 digits: Sequential number (odd for males, even for females)
- Last digit: Check digit

## Limitations

- Only generates PESELs for years between 1800 and 2299
- Sequential numbers range from 0000 to 9999
- Month encoding follows PESEL rules for different centuries:
  - 1800-1899: add 80 to month
  - 1900-1999: no modification
  - 2000-2099: add 20 to month
  - 2100-2199: add 40 to month
  - 2200-2299: add 60 to month

## Note

This tool is for educational and testing purposes only. Generated PESEL numbers should not be used for any official purposes.
