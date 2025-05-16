# dso-geo-coordinate-fuzzer
Adds random noise to latitude and longitude coordinates, creating a circular area of uncertainty around each point. Useful for de-identifying location data without completely removing geographic information. - Focused on Tools for sanitizing and obfuscating sensitive data within text files and structured data formats

## Install
`git clone https://github.com/ShadowStrikeHQ/dso-geo-coordinate-fuzzer`

## Usage
`./dso-geo-coordinate-fuzzer [params]`

## Parameters
- `--radius`: No description provided
- `--lat_col`: No description provided
- `--lon_col`: No description provided
- `--delimiter`: No description provided
- `--header`: If the input file contains a header row, skip it.
- `--encoding`: Encoding of the input file. If not provided, it will be detected automatically.

## License
Copyright (c) ShadowStrikeHQ
