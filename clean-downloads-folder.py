import logging
from pathlib import Path
import os
import shutil
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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

def handle_cover_letter_pdf(path: Path):
    for f in DOWNLOADS.glob("*"):
        try:
            if f.is_file() and SPECIAL_CL_NAME in f.name and f != path:
                f.unlink()
                logging.info(f"Deleted old cover letter: {f.name}")
        except Exception as e:
            logging.warning(f"Failed to delete {f.name}: {e}")

    target = DOWNLOADS / f"{SPECIAL_CL_NAME}.pdf"
    if target.exists() and target!=path:
        try:
            target.unlink()
            logging.info(f"Removed existing {target.name} to enforce exact name")
        except Exception as e:
            logging.error(f"Rename to '{target.name} failed: {e}")

def categorize_file(path: Path):
    if not path.is_file():
        return
    ext = path.suffix.lower()

    # PDFs
    if ext == ".pdf":
        if SPECIAL_CL_NAME in path.name:
            handle_cover_letter_pdf()
        else:
            safe_move(path, "PDFs")
        return
    
    # recognized non-PDFs
    for folder, exts in FOLDERS.items():
        if ext in exts:
            safe_move(path, folder)
            return
    
    # all others
    safe_move(path, "Other")

def scan_existing_files():
    for p in DOWNLOADS.itedir():
        if p.is_file():
            categorize_file(p)

class DownloadsHandler(FileSystemEventHandler):
    def on_created(self, event):
        time.sleep(2)
        path = Path(event.src_path)
        categorize_file(path)

if __name__ == "__main__":
    ensure_folders()
    scan_existing_files()

    observer = Observer()
    observer.schedule(DownloadsHandler(), str(DOWNLOADS), recursive=False)
    observer.start()
    
    logging.info(f"Watching folder: {DOWNLOADS}")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()