import os, re, io, tempfile
import pandas as pd

# ---- Try PDF text first (pdfminer.six), else OCR with pdf2image + pytesseract ----
# Install (one time):
#   pip install pdfminer.six pdf2image pillow pytesseract
# System reqs:
#   Tesseract OCR:  macOS: brew install tesseract
#                   Ubuntu/Debian: sudo apt-get install tesseract-ocr
#   Poppler (for pdf2image): macOS: brew install poppler
#                            Ubuntu/Debian: sudo apt-get install poppler-utils

from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# --------- Regex (tolerant to spaces/hyphens/line-wrapping) ----------
RE_ASSET     = re.compile(r"Asset\s+A[-\s]?(\d+)", re.I)
RE_LOCATION  = re.compile(r"Location:\s*(.*)", re.I)
RE_DEFECT    = re.compile(r"Defect\s+D[-\s]?(\d+)\s+for\s+A[-\s]?(\d+)", re.I)
RE_SUBTOTAL  = re.compile(r"Subtotal:\s*\$?\s*([\d,\s]*\d(?:\.\d{1,2})?)", re.I)

def _clean(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    # glue split currency like "$ 2,340.00"
    text = re.sub(r"(\$)\s+(\d)", r"\1\2", text)
    return text

def _lines(text: str):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]

def parse_lines(lines):
    """Parse lines into defect rows."""
    rows = []
    current_location = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Capture latest Location (may spill one line)
        m_loc = RE_LOCATION.search(line)
        if m_loc:
            loc = m_loc.group(1).strip()
            if i + 1 < len(lines) and not (
                RE_DEFECT.search(lines[i+1]) or RE_ASSET.search(lines[i+1]) or RE_LOCATION.search(lines[i+1])
            ):
                loc += " " + lines[i+1].strip()
            current_location = loc

        m_def = RE_DEFECT.search(line)
        if m_def:
            defect_id, asset_id = m_def.groups()

            # Gather description until Subtotal or another block header
            desc = []
            j = i + 1
            while j < len(lines) and not (
                RE_SUBTOTAL.search(lines[j]) or RE_DEFECT.search(lines[j]) or RE_ASSET.search(lines[j]) or RE_LOCATION.search(lines[j])
            ):
                desc.append(lines[j])
                j += 1
            description = " ".join(desc).strip()

            subtotal = None
            if j < len(lines):
                m_sub = RE_SUBTOTAL.search(lines[j])
                if m_sub:
                    amt = m_sub.group(1).replace(",", "").replace(" ", "")
                    try:
                        subtotal = float(amt)
                    except ValueError:
                        subtotal = None

            rows.append({
                "Defect ID": defect_id,
                "Asset ID":  asset_id,
                "Description": description,
                "Subtotal": subtotal,
                "Location": current_location
            })
            i = j
            continue

        i += 1

    return rows

def pdf_to_text_pages(pdf_path: str):
    """Return list of per-page text using pdfminer; pages with little text become ''."""
    text = extract_text(pdf_path) or ""
    # pdfminer returns whole doc; split heuristically on form feed if present
    pages = [p for p in text.split("\f") if p.strip()] or [text]
    return [_clean(p) for p in pages]

def ocr_pdf_pages(pdf_path: str, dpi=300, psm="6", oem="3"):
    """OCR each page to text."""
    pil_pages = convert_from_path(pdf_path, dpi=dpi)
    out = []
    for img in pil_pages:
        # Basic binarization to help OCR
        gray = img.convert("L")
        out.append(
            pytesseract.image_to_string(gray, config=f"--oem {oem} --psm {psm}")
        )
    return [_clean(t) for t in out]

def convert(pdf_path: str, out_csv="fireinspection_master.csv", out_xlsx="fireinspection.xlsx"):
    # 1) Try native text first
    pages_text = pdf_to_text_pages(pdf_path)
    rows = []
    for t in pages_text:
        rows += parse_lines(_lines(t))

    # 2) If too few rows, fallback to OCR (some PDFs are scanned)
    if len(rows) < 20:  # heuristic threshold given document says 41 defects
        rows = []  # reset and rely on OCR
        for psm in ("6", "4", "11"):  # try a few PSMs
            ocr_pages = ocr_pdf_pages(pdf_path, dpi=300, psm=psm, oem="3")
            rows_tmp = []
            for t in ocr_pages:
                rows_tmp += parse_lines(_lines(t))
            if len(rows_tmp) > len(rows):
                rows = rows_tmp
            if len(rows) >= 41:
                break

    df = pd.DataFrame(rows, columns=["Defect ID","Asset ID","Description","Subtotal","Location"])
    df.to_csv(out_csv, index=False)
    df.to_excel(out_xlsx, index=False)
    return df

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Convert fire inspection PDF to Excel/CSV (with OCR fallback).")
    ap.add_argument("pdf", help="Path to PDF (e.g., fireinspection.pdf)")
    ap.add_argument("--csv", default="fireinspection_master.csv")
    ap.add_argument("--xlsx", default="fireinspection.xlsx")
    args = ap.parse_args()

    df = convert(args.pdf, args.csv, args.xlsx)
    print(f"Done. Parsed {len(df)} defects -> {args.csv}, {args.xlsx}")
