import argparse
import os
import re
import subprocess
from pathlib import Path

import pandas as pd
from PIL import Image
import pytesseract

KAGGLE_DATASET = "senju14/invoice-ocr"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def ensure_tesseract_installed() -> bool:
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, text=True, check=True)
        return True
    except Exception:
        return False


def download_kaggle_dataset(target_dir: Path) -> Path:
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        raise RuntimeError("Python package kaggle is not installed.")

    target_dir.mkdir(parents=True, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(KAGGLE_DATASET, path=str(target_dir), unzip=True, quiet=False)
    return target_dir


def get_image_paths(folder: Path) -> list[Path]:
    return sorted([p for p in folder.rglob("*") if p.suffix.lower() in IMAGE_EXTS])


def extract_text_from_image(image_path: Path) -> str:
    with Image.open(image_path) as img:
        return pytesseract.image_to_string(img, lang="eng")


def save_extracted_text(image_path: Path, text: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_txt = output_dir / (image_path.stem + ".txt")
    output_txt.write_text(text, encoding="utf-8")
    return output_txt


def parse_invoice_text(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_text = "\n".join(lines)

    invoice_number = None
    company_name = None
    customer_name = None
    date = None
    total_amount = None

    invoice_patterns = [r"Invoice\s*No\.?\s*[:\-]?\s*(\S+)",
                        r"Inv(?:oice)?\s*#\s*[:\-]?\s*(\S+)",
                        r"Invoice\s*Number\s*[:\-]?\s*(\S+)"]
    for pat in invoice_patterns:
        match = re.search(pat, full_text, re.IGNORECASE)
        if match:
            invoice_number = match.group(1)
            break

    date_patterns = [r"(\d{1,2}/\d{1,2}/\d{2,4})",
                     r"(\d{1,2}-\d{1,2}-\d{2,4})",
                     r"(\d{4}-\d{1,2}-\d{1,2})"]
    for pat in date_patterns:
        match = re.search(pat, full_text)
        if match:
            date = match.group(1)
            break

    total_patterns = [r"Total\s+Amount\s*[:\-]?\s*\$?([\d,]+\.\d{2})",
                      r"Grand\s+Total\s*[:\-]?\s*\$?([\d,]+\.\d{2})",
                      r"Amount\s+Due\s*[:\-]?\s*\$?([\d,]+\.\d{2})",
                      r"Total\s*[:\-]?\s*\$?([\d,]+\.\d{2})"]
    for pat in total_patterns:
        match = re.search(pat, full_text, re.IGNORECASE)
        if match:
            total_amount = match.group(1)
            break

    customer_patterns = [r"Bill\s+To\s*[:\-]?\s*(.+)",
                         r"Customer\s*[:\-]?\s*(.+)",
                         r"Ship\s+To\s*[:\-]?\s*(.+)"]
    for pat in customer_patterns:
        match = re.search(pat, full_text, re.IGNORECASE)
        if match:
            customer_name = match.group(1).strip()
            customer_name = re.split(r"\n|\r|\.|,", customer_name)[0].strip()
            break

    if lines:
        company_name = lines[0]
        if any(keyword.lower() in company_name.lower() for keyword in ["invoice", "date", "customer", "bill", "total"]):
            company_name = lines[1] if len(lines) > 1 else company_name

    return {
        "file_name": None,
        "invoice_number": invoice_number,
        "company_name": company_name,
        "date": date,
        "customer_name": customer_name,
        "total_amount": total_amount,
        "raw_text": full_text,
    }


def process_invoice_images(image_dir: Path, text_dir: Path, max_images: int = 5) -> pd.DataFrame:
    image_paths = get_image_paths(image_dir)[:max_images]
    if not image_paths:
        raise FileNotFoundError(f"No invoice images found in {image_dir}")

    rows = []
    for image_path in image_paths:
        print(f"Processing {image_path.name}")
        text = extract_text_from_image(image_path)
        save_extracted_text(image_path, text, text_dir)
        parsed = parse_invoice_text(text)
        parsed["file_name"] = image_path.name
        rows.append(parsed)

    df = pd.DataFrame(rows)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoice OCR extraction and parsing")
    parser.add_argument("--images", type=Path, default=Path("invoice_images"), help="Folder containing invoice images")
    parser.add_argument("--output", type=Path, default=Path("invoice_output"), help="Folder to save OCR text files and outputs")
    parser.add_argument("--download", action="store_true", help="Download the Kaggle invoice OCR dataset if Kaggle credentials are available")
    parser.add_argument("--max", type=int, default=5, help="Maximum number of images to process")
    args = parser.parse_args()

    if args.download:
        print("Downloading Kaggle dataset...")
        try:
            download_kaggle_dataset(Path("invoice_dataset"))
            print("Download complete.")
        except Exception as exc:
            print("Failed to download dataset:", exc)
            print("Make sure Kaggle credentials are configured in ~/.kaggle/kaggle.json or KAGGLE_USERNAME/KAGGLE_KEY are set.")
            return

    if not ensure_tesseract_installed():
        print("Tesseract OCR is not installed or not on PATH.")
        print("Install Tesseract on Windows using the installer from https://github.com/tesseract-ocr/tesseract or use winget.")
        return

    output_text_dir = args.output / "texts"
    summary_path = args.output / "invoice_summary.csv"
    df = process_invoice_images(args.images, output_text_dir, max_images=args.max)
    args.output.mkdir(parents=True, exist_ok=True)
    df.to_csv(summary_path, index=False)
    print(f"Saved invoice summary to {summary_path}")


if __name__ == "__main__":
    main()
