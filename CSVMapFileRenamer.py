#!/usr/bin/env python3
"""
File Renamer with CSV Mapping
Uses Gooey to provide a GUI for renaming files based on CSV key-value mapping.

Required dependencies:
pip install gooey pandas

CSV format expected:
Column 1: Current filename (key)
Column 2: New filename (target)
"""

import os
import sys
import pandas as pd
import logging
from pathlib import Path
from gooey import Gooey, GooeyParser

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@Gooey(
    program_name="File Renamer with CSV Mapping",
    program_description="Rename files in a folder based on CSV key-value mapping",
    default_size=(600, 500),
    required_cols=2,
    optional_cols=1,
    #richtext_controls=True,
    show_success_modal=True,
    show_failure_modal=True,
    navigation='SIDEBAR'
)
def main():
    parser = GooeyParser(description="Rename files using a CSV map")

    # Input folder selection
    parser.add_argument(
        'input_folder',
        metavar='Input Folder',
        help='Folder containing files to rename',
        widget='DirChooser'
    )

    # CSV file selection
    parser.add_argument(
        'csv_file',
        metavar='CSV Map File',
        help='CSV file with current names (column 1) and target names (column 2)',
        widget='FileChooser',
        gooey_options={
            'wildcard': "CSV files (*.csv)|*.csv|All files (*.*)|*.*"
        }
    )

    # Optional: backup option
    parser.add_argument(
        '--create_backup',
        action='store_true',
        help='Create backup copies of original files before renaming',
        default=False
    )

    # Optional: dry run
    parser.add_argument(
        '--dry_run',
        action='store_true',
        help='Preview changes without actually renaming files',
        default=False
    )

    # Optional: case sensitive matching
    parser.add_argument(
        '--case_sensitive',
        action='store_true',
        help='Use case-sensitive filename matching',
        default=False
    )

    args = parser.parse_args()

    try:
        # Validate inputs
        input_folder = Path(args.input_folder)
        csv_file = Path(args.csv_file)

        if not input_folder.exists():
            raise FileNotFoundError(f"Input folder does not exist: {input_folder}")

        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file does not exist: {csv_file}")

        # Read CSV mapping
        logger.info(f"Reading CSV mapping from: {csv_file}")
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

        if df.shape[1] < 2:
            raise ValueError("CSV file must have at least 2 columns")

        # Use first two columns regardless of their names
        key_col = df.columns[0]
        target_col = df.columns[1]

        # Create mapping dictionary
        if args.case_sensitive:
            mapping = dict(zip(df[key_col].astype(str), df[target_col].astype(str)))
        else:
            mapping = dict(zip(df[key_col].astype(str).str.lower(), df[target_col].astype(str)))

        logger.info(f"Loaded {len(mapping)} mappings from CSV")

        # Get all files in input folder
        all_files = [f for f in input_folder.iterdir() if f.is_file()]
        logger.info(f"Found {len(all_files)} files in input folder")

        # Find files to rename
        files_to_rename = []
        for file_path in all_files:
            filename = file_path.name
            search_key = filename if args.case_sensitive else filename.lower()

            if search_key in mapping:
                new_name = mapping[search_key]
                files_to_rename.append((file_path, new_name))

        if not files_to_rename:
            logger.warning("No files found that match the CSV mapping")
            print("No files found that match the CSV mapping.")
            return

        logger.info(f"Found {len(files_to_rename)} files to rename")

        # Preview or execute renaming
        success_count = 0
        error_count = 0

        if args.dry_run:
            print("DRY RUN - Preview of changes:")
            print("-" * 50)
            for old_path, new_name in files_to_rename:
                print(f"'{old_path.name}' -> '{new_name}'")
            print("-" * 50)
            print(f"Total files to rename: {len(files_to_rename)}")
        else:
            print("Renaming files...")
            print("-" * 50)

            for old_path, new_name in files_to_rename:
                try:
                    # Create new path
                    new_path = old_path.parent / new_name

                    # Check if target file already exists
                    if new_path.exists() and new_path != old_path:
                        logger.warning(f"Target file already exists: {new_name}")
                        print(f"SKIPPED: '{old_path.name}' -> '{new_name}' (target exists)")
                        error_count += 1
                        continue

                    # Create backup if requested
                    if args.create_backup:
                        backup_path = old_path.parent / f"{old_path.name}.backup"
                        old_path.rename(backup_path)
                        backup_path.rename(new_path)
                    else:
                        old_path.rename(new_path)

                    print(f"RENAMED: '{old_path.name}' -> '{new_name}'")
                    success_count += 1

                except Exception as e:
                    logger.error(f"Error renaming {old_path.name}: {e}")
                    print(f"ERROR: Failed to rename '{old_path.name}': {e}")
                    error_count += 1

        # Summary
        print("-" * 50)
        if args.dry_run:
            print(f"Preview completed: {len(files_to_rename)} files would be renamed")
        else:
            print(f"Renaming completed: {success_count} successful, {error_count} errors")
            if args.create_backup:
                print("Note: Backup files were created with .backup extension")

    except Exception as e:
        logger.error(f"Program error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
