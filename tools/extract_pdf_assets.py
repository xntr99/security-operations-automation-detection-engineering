"""Extract text and embedded images from the SOC automation lab PDF.

Usage:
    python tools/extract_pdf_assets.py "C:/path/to/source-lab.pdf"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader


def normalize_text(text: str) -> str:
    return (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2022", "-")
        .strip()
    )


def extract(pdf_path: Path, repo_root: Path) -> None:
    reader = PdfReader(str(pdf_path))
    docs_dir = repo_root / "docs"
    image_dir = repo_root / "assets" / "images"
    docs_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    source_lines = [
        f"# Source Extract: {pdf_path.name}",
        "",
        f"Pages: {len(reader.pages)}",
        "",
    ]
    manifest_lines = [
        "# Image Manifest",
        "",
        "| Page | Image | File |",
        "|---:|---:|---|",
    ]

    image_count = 0
    for page_number, page in enumerate(reader.pages, 1):
        text = normalize_text(page.extract_text() or "")
        source_lines.extend(
            [
                f"## Page {page_number}",
                "",
                text if text else "_No extractable text on this page._",
                "",
            ]
        )

        for image_number, image in enumerate(page.images, 1):
            suffix = Path(image.name).suffix.lower() or ".bin"
            filename = f"page-{page_number:02d}-image-{image_number:02d}{suffix}"
            (image_dir / filename).write_bytes(image.data)
            manifest_lines.append(
                f"| {page_number} | {image_number} | "
                f"[`{filename}`](../assets/images/{filename}) |"
            )
            image_count += 1

    (docs_dir / "source-extract.md").write_text("\n".join(source_lines), encoding="utf-8")
    (docs_dir / "image-manifest.md").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(f"Extracted {len(reader.pages)} pages and {image_count} images.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path, help="Path to the source PDF.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root where docs/ and assets/ should be written.",
    )
    args = parser.parse_args()
    extract(args.pdf, args.repo_root)


if __name__ == "__main__":
    main()
