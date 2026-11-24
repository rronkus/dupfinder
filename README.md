# dupfinder

A lightweight Python command-line tool for finding duplicate files using SHA-256 hashing.

## Features

- Finds identical files using SHA-256.
- Scans directories recursively.
- Groups duplicate files together.
- Checks file sizes before hashing.
- Displays file sizes and duplicate groups.
- Handles inaccessible files without stopping the scan.
- Does not modify or delete files.
- No external dependencies.

## Usage

Run the following command:

```bash
python dupfinder.py "path/to/directory"
```

For example:

```bash
python dupfinder.py "E:\Documents"
```

## Example output

```text
dupfinder

Scanning: E:\Documents

Duplicate files:

  Group 1 (12.4 KB):
    E:\Documents\report.pdf
    E:\Documents\report-copy.pdf

1 duplicate groups found.
24 files examined.
```

## Tests

Run the automated tests:

```bash
python -m unittest -v
```

## Requirements

- Python 3.10 or newer
- No third-party packages

## How it works

1. Scans the selected directory and its subdirectories.
2. Groups files by their size.
3. Calculates SHA-256 hashes for files with matching sizes.
4. Groups files with identical hashes.

## License

MIT
