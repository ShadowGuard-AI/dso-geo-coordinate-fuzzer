#!/usr/bin/env python3

import argparse
import logging
import random
import math
import sys
import chardet

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description='Fuzzes latitude and longitude coordinates by adding random noise.')
    parser.add_argument('input_file', type=str, help='Path to the input file containing coordinates.')
    parser.add_argument('output_file', type=str, help='Path to the output file to write the fuzzed coordinates.')
    parser.add_argument('--radius', type=float, default=0.01, help='Radius of the uncertainty circle in degrees (default: 0.01).')
    parser.add_argument('--lat_col', type=int, default=0, help='Column index for latitude (0-based, default: 0).')
    parser.add_argument('--lon_col', type=int, default=1, help='Column index for longitude (0-based, default: 1).')
    parser.add_argument('--delimiter', type=str, default=',', help='Delimiter used in the input file (default: comma).')
    parser.add_argument('--header', action='store_true', help='If the input file contains a header row, skip it.')
    parser.add_argument('--encoding', type=str, default=None, help='Encoding of the input file. If not provided, it will be detected automatically.')

    return parser.parse_args()

def fuzz_coordinate(latitude, longitude, radius):
    """
    Adds random noise to a coordinate pair.

    Args:
        latitude (float): The latitude.
        longitude (float): The longitude.
        radius (float): The radius of uncertainty in degrees.

    Returns:
        tuple: A tuple containing the fuzzed latitude and longitude.
    """
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        logging.error(f"Invalid latitude or longitude: latitude={latitude}, longitude={longitude}")
        raise ValueError("Latitude and longitude must be numeric values.")

    # Input Validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    if radius <= 0:
        raise ValueError("Radius must be greater than 0")


    # Generate a random angle and distance within the radius
    angle = 2 * math.pi * random.random()
    distance = radius * math.sqrt(random.random())  # sqrt for uniform distribution within the circle

    # Calculate the new coordinates
    new_latitude = latitude + distance * math.sin(angle)
    new_longitude = longitude + distance * math.cos(angle)

    # Clip new lat/lon to acceptable range
    new_latitude = max(-90, min(90, new_latitude))
    new_longitude = max(-180, min(180, new_longitude))

    return new_latitude, new_longitude

def process_file(input_file, output_file, radius, lat_col, lon_col, delimiter, header, encoding):
    """
    Processes the input file, fuzzes the coordinates, and writes the output to a file.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to the output file.
        radius (float): Radius of the uncertainty circle in degrees.
        lat_col (int): Column index for latitude.
        lon_col (int): Column index for longitude.
        delimiter (str): Delimiter used in the input file.
        header (bool): Whether the input file contains a header row.
        encoding (str): Encoding of the input file.

    Raises:
        FileNotFoundError: If the input file is not found.
        IOError: If there's an error reading or writing files.
        ValueError: If invalid data is encountered.
    """

    try:
        # Detect encoding if not provided
        if not encoding:
            with open(input_file, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
                logging.info(f"Detected encoding: {encoding}")

        with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w', encoding=encoding) as outfile:
            
            if header:
                #Skip the header row
                next(infile)

            for line_number, line in enumerate(infile, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    parts = line.split(delimiter)
                    if len(parts) <= max(lat_col, lon_col):
                        logging.warning(f"Skipping line {line_number}: Not enough columns. Columns found: {len(parts)}")
                        outfile.write(line + '\n')  # Write the original line to the output
                        continue

                    latitude = parts[lat_col]
                    longitude = parts[lon_col]
                    
                    new_latitude, new_longitude = fuzz_coordinate(latitude, longitude, radius)

                    parts[lat_col] = str(new_latitude)
                    parts[lon_col] = str(new_longitude)

                    outfile.write(delimiter.join(parts) + '\n')
                except ValueError as e:
                    logging.error(f"Error processing line {line_number}: {e}")
                    outfile.write(line + '\n')  # Write the original line to the output

    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        raise
    except IOError as e:
        logging.error(f"IOError: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise


def main():
    """
    Main function to parse arguments and process the file.
    """
    try:
        args = setup_argparse()
        process_file(args.input_file, args.output_file, args.radius, args.lat_col, args.lon_col, args.delimiter, args.header, args.encoding)
        logging.info("File processed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()