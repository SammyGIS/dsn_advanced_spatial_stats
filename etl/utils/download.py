import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
import requests
from config import get_logger

logger = get_logger("Utils_Download")


def _download_chunks(response: requests.Response, temp_dest: str) -> int:
    """Helper to download a file in chunks and write to disk."""
    downloaded = 0
    with open(temp_dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=2 * 1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
    return downloaded

def download_file(url: str, dest_path: str, min_expected_mb: float = 1.0) -> str:
    """Download a remote file with streaming progress and write status to log.txt."""
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    filename = os.path.basename(dest_path)

    if os.path.exists(dest_path) and os.path.getsize(dest_path) > min_expected_mb * 1024 * 1024:
        logger.info(f"{filename} already exists ({os.path.getsize(dest_path) / 1e6:.1f} MB). Skipping download.")
        return dest_path

    logger.info(f"Starting download of {filename} from {url[:70]}...")
    t0 = time.time()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    temp_dest = dest_path + ".part"

    with requests.get(url, stream=True, headers=headers, timeout=300) as r:
        r.raise_for_status()
        _download_chunks(r, temp_dest)

    if os.path.exists(dest_path):
        os.remove(dest_path)
    os.rename(temp_dest, dest_path)
    duration = time.time() - t0
    logger.info(f"Successfully downloaded {filename} ({os.path.getsize(dest_path) / 1e6:.1f} MB) in {duration:.2f}s")
    return dest_path
