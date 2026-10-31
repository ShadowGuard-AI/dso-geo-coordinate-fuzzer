![Banner](banner.png)

# dso-geo-coordinate-fuzzer
Adds random noise to latitude and longitude coordinates, creating a circular area of uncertainty around each point. Useful for de-identifying location data without completely removing geographic information. - Focused on Tools for sanitizing and obfuscating sensitive data within text files and structured data formats

## Install
`git clone https://github.com/ShadowStrikeHQ/dso-geo-coordinate-fuzzer`

## Usage
`./dso-geo-coordinate-fuzzer [params]`

## Parameters
- `--radius`: Radius of the uncertainty circle in degrees (default: 0.01). Must be greater than 0; a radius of 0 or negative is rejected with exit 1 before any processing.
- `--lat_col`: Column index for latitude (0-based, default: 0).
- `--lon_col`: Column index for longitude (0-based, default: 1).
- `--delimiter`: Delimiter used in the input file (default: comma).
- `--header`: If the input file contains a header row, it is written to the output unchanged and is not fuzzed.
- `--encoding`: Encoding of the input file. If not provided, it will be detected automatically.

## Behavior notes
- The output file must not be the input file. If the resolved output path equals the resolved input path (same string, a ./ alias, or a symlink), the run refuses with exit 1 before any file is opened, and the input is left unchanged.
- Rows that cannot be fuzzed (non numeric, too few columns, or out of range coordinates) are dropped from the output instead of being copied with their original coordinates. The run logs how many rows were dropped and exits 1 when any row was dropped; the output is still written from the valid fuzzed rows.
- Longitude wraps across the antimeridian and latitude reflects at the poles, so fuzzed points stay inside the valid ranges without collecting on the boundary lines.
- An input with no data rows exits non-zero with a "No rows fuzzed." message instead of reporting success.

## License
Copyright (c) ShadowStrikeHQ
