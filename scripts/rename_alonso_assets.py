#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


DEFAULT_FOLDER_CANDIDATES = [
    Path(
        "opti_papers/"
        "alonso-mora-et-al-2017-on-demand-high-capacity-ride-sharing-via-dynamic-trip-vehicle-assignment__assets"
    ),
    Path(
        "opti_papers/"
        "alonso_mora_et_al_2017_on_demand_high_capacity_ride_sharing_via_dynamic_trip_vehicle_assignment_assets"
    ),
]

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}


def sanitize_folder_name(name: str) -> str:
    """Convert name to contain only ASCII letters, digits, and underscores."""
    sanitized = re.sub(r"[^0-9A-Za-z_]", "_", name)
    sanitized = re.sub(r"_+", "_", sanitized)
    sanitized = sanitized.strip("_")
    return sanitized or "assets"


def rename_folder(folder: Path) -> Path:
    sanitized_name = sanitize_folder_name(folder.name)
    target = folder.parent / sanitized_name
    if target == folder:
        return folder
    if target.exists():
        raise RuntimeError(f"Target folder already exists: {target}")
    folder.rename(target)
    return target


def iter_image_files(folder: Path):
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def rename_images(folder: Path) -> list[tuple[Path, Path]]:
    renames: list[tuple[Path, Path]] = []
    for index, source in enumerate(iter_image_files(folder), start=1):
        suffix = source.suffix.lower()
        target = folder / f"fig{index}{suffix}"
        renames.append((source, target))

    temp_renames: list[tuple[Path, Path]] = []
    for idx, (source, target) in enumerate(renames, start=1):
        if source == target:
            continue
        temp = source.with_name(f"__tmp__{idx}__{source.name}")
        if temp.exists():
            raise RuntimeError(f"Temporary path already exists: {temp}")
        source.rename(temp)
        temp_renames.append((temp, target))

    for temp, target in temp_renames:
        if target.exists():
            raise RuntimeError(f"Target file already exists: {target}")
        temp.rename(target)

    return renames


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename Alonso-Mora asset folder and files.")
    parser.add_argument(
        "folder",
        nargs="?",
        help="Path to the assets folder to rename.",
    )
    args = parser.parse_args()

    if args.folder is not None:
        folder = Path(args.folder)
    else:
        for candidate in DEFAULT_FOLDER_CANDIDATES:
            if candidate.exists():
                folder = candidate
                break
        else:
            raise SystemExit(
                "Unable to locate assets folder automatically. Provide it explicitly."
            )

    if not folder.exists():
        raise SystemExit(f"Folder not found: {folder}")
    if not folder.is_dir():
        raise SystemExit(f"Provided path is not a directory: {folder}")

    folder = rename_folder(folder)
    renames = rename_images(folder)

    print(folder)
    for source, target in renames:
        print(f"{source.name} -> {target.name}")


if __name__ == "__main__":
    main()
