import logging
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
FOLDERS = {
    "PDFs": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg", ".heic", ".ico"],
    "Sounds": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff", ".alac", ".opus"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v", ".3gp"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Apps": [".exe", ".dmg", ".apk", ".bat"],
    "Documents": [".doc", ".docx", ".txt", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
}

SPECIAL_CL_NAME = "Cover Letter_AV"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def ensure_folders():
    for folder in list(FOLDERS.keys()) + ["Other"]:
        path = DOWNLOADS / folder
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Ready. Downloads path: {DOWNLOADS}")

if __name__ == "__main__":
    ensure_folders()
    logging.info(f"Ready. Downloads path: {DOWNLOADS}")

