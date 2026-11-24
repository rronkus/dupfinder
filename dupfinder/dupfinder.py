
import argparse
import hashlib
import os
import sys
from collections import defaultdict
from pathlib import Path


CHUNK_SIZE = 1024 * 1024


def file_hash(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            digest.update(chunk)

    return digest.hexdigest()


def find_duplicates(root):
    files_by_size = defaultdict(list)
    examined = 0
    errors = 0

    def handle_error(error):
        nonlocal errors
        errors += 1

    for directory, subdirs, filenames in os.walk(
        root, onerror=handle_error, followlinks=False
    ):
        subdirs[:] = [
            name for name in subdirs
            if not (Path(directory) / name).is_symlink()
        ]

        for filename in filenames:
            path = Path(directory) / filename

            try:
                if path.is_symlink() or not path.is_file():
                    continue

                size = path.stat().st_size
                files_by_size[size].append(path)
                examined += 1

            except OSError:
                errors += 1

    hashes = defaultdict(list)

    for size, paths in files_by_size.items():
        if len(paths) < 2:
            continue

        for path in paths:
            try:
                digest = file_hash(path)
                hashes[(size, digest)].append(path)

            except OSError:
                errors += 1

    duplicates = [
        paths for paths in hashes.values()
        if len(paths) > 1
    ]

    return duplicates, examined, errors


def format_size(size):
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"

        value /= 1024

    return f"{value:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files using SHA-256."
    )

    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan recursively."
    )

    args = parser.parse_args()
    root = args.directory.expanduser()

    if not root.exists() or not root.is_dir():
        print(
            f"Error: directory not found: {root}",
            file=sys.stderr
        )
        return 2

    print("dupfinder")
    print()
    print(f"Scanning: {root.resolve()}")
    print()

    duplicates, examined, errors = find_duplicates(root)

    if duplicates:
        print("Duplicate files:")
        print()

        for index, group in enumerate(duplicates, 1):
            size = group[0].stat().st_size

            print(f"  Group {index} ({format_size(size)}):")

            for path in group:
                print(f"    {path}")

            print()

    else:
        print("No duplicate files found.")
        print()

    print(f"{len(duplicates)} duplicate groups found.")
    print(f"{examined} files examined.")

    if errors:
        print(f"{errors} files or directories could not be read.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
