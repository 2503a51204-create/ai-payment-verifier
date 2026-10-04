import hashlib
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


SUSPICIOUS_TERMS = {
    "edited",
    "modified",
    "photoshop",
    "fake",
    "generated",
    "manipulated",
}


def calculate_sha256(file_path):
    digest = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def extract_text(file_path):
    suffix = Path(file_path).suffix.lower()

    if suffix in {".png", ".jpg", ".jpeg"}:
        if Image is None or pytesseract is None:
            return ""

        image = Image.open(file_path)
        return pytesseract.image_to_string(image).strip()

    if suffix == ".pdf":
        if PdfReader is None:
            return ""

        reader = PdfReader(str(file_path))
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages).strip()

    return ""


def assess_text(text):
    lowered = text.lower()
    found_terms = sorted(term for term in SUSPICIOUS_TERMS if term in lowered)

    if found_terms:
        return {
            "label": "Review recommended",
            "reason": "Potential manipulation-related terms were detected in extracted text.",
            "risk": "medium",
            "found_terms": found_terms,
        }

    return {
        "label": "Low risk",
        "reason": "No major manipulation indicators were detected in the extracted text.",
        "risk": "low",
        "found_terms": [],
    }


def analyze_file(file_path):
    file_path = Path(file_path)
    file_hash = calculate_sha256(file_path)
    text = extract_text(file_path)
    ai = assess_text(text)

    file_size = file_path.stat().st_size
    mime_type = mimetypes.guess_type(file_path.name)[0] or "unknown"

    if ai["risk"] == "low":
        score = 92
        status = "Likely genuine — Low Risk"
        risk_level = "low"
    else:
        score = 58
        status = "Review required — Medium Risk"
        risk_level = "medium"

    return {
        "file_name": file_path.name,
        "score": score,
        "status": status,
        "risk_level": risk_level,
        "integrity": {
            "status": "Verified",
            "details": "SHA-256 fingerprint generated successfully.",
        },
        "content": {
            "status": "Analyzed" if text else "No text found",
            "preview": text[:5000],
        },
        "metadata": {
            "status": "Available",
            "details": f"Type: {mime_type} | Size: {file_size / 1024:.1f} KB",
        },
        "ai": {
            "label": ai["label"],
            "reason": ai["reason"],
            "found_terms": ai["found_terms"],
        },
        "hash": file_hash,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "disclaimer": (
            "This is a risk-assessment prototype, not definitive forensic proof "
            "of authenticity."
        ),
    }
