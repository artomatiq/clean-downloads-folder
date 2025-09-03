import logging
from pathlib import Path
import os
import shutil

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

def safe_move(src: Path, dest_folder_name: str) -> Path:
    dest_folder = DOWNLOADS /dest_folder_name
    dest_folder.mkdir(exists_ok=True)
    dest = dest_folder / src.name
    base, ext = os.path.splitext(dest.name)
    i = 1
    while dest.exists():
        dest = dest_folder / f"{base} ({i}){ext}"
        i += 1
    shutil.move(str(src), str(dest))
    logging.info(f"Moved {src.name} -> {dest}")
    return dest

def categorize_file(path: Path):
    if not path.is_file():
        return
    ext = path.suffix.lower()

    # PDFs
    if ext == ".pdf":
        safe_move(path, "PDFs")
        return
    
    # recognized non-PDFs
    for folder, exts in FOLDERS.items():
        if ext in exts:
            safe_move(path, folder)
            return
    
    # all others
    safe_move(path, "Other")

