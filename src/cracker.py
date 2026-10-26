"""Module điều phối tiến trình quét mật khẩu (Wordlist & Brute-force song song)."""

import itertools
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from src.config import DEFAULT_SETTINGS, Settings
from src.crypto import CryptoParams, verify_password

log = logging.getLogger(__name__)


def check_prefix(
    prefix: str,
    length: int,
    chars: str,
    crypto: CryptoParams,
) -> str | None:
    """Kiểm tra toàn bộ tổ hợp mật khẩu bắt đầu bằng prefix cho một độ dài."""
    for rest in itertools.product(chars, repeat=length - 1):
        pwd = prefix + "".join(rest)
        if verify_password(pwd, crypto):
            return pwd
    return None


def phase_wordlist(wordlist_path: Path, crypto: CryptoParams) -> str | None:
    """Phase 1: Quét danh sách mật khẩu dạng wordlist nếu tồn tại."""
    if not wordlist_path.is_file():
        log.debug("Không tìm thấy wordlist tại '%s'. Bỏ qua Phase 1.", wordlist_path)
        return None

    log.info("Phase 1: Quét Wordlist '%s'...", wordlist_path)
    t0 = time.time()
    try:
        with wordlist_path.open("r", encoding="utf-8", errors="ignore") as f:
            for tried, line in enumerate(f, start=1):
                pwd = line.strip()
                if not pwd:
                    continue
                if tried % 50_000 == 0:
                    rate = tried / max(time.time() - t0, 0.001)
                    log.info(
                        "Đã thử: %s | Tốc độ: %s pwd/s | Hiện tại: '%s'",
                        f"{tried:,}",
                        f"{rate:,.0f}",
                        pwd,
                    )
                if verify_password(pwd, crypto):
                    return pwd
    except OSError as err:
        log.error("Lỗi khi đọc wordlist '%s': %s", wordlist_path, err)
        return None

    log.info("Wordlist hoàn thành. Không tìm thấy mật khẩu.")
    return None


def phase_bruteforce(
    crypto: CryptoParams,
    settings: Settings = DEFAULT_SETTINGS,
) -> str | None:
    """Phase 2: Brute-force song song đa tiến trình qua ProcessPoolExecutor."""
    log.info(
        "Phase 2: Brute-force song song (%d CPU cores | Độ dài 1 đến %d)",
        settings.num_workers,
        settings.max_length,
    )

    with ProcessPoolExecutor(max_workers=settings.num_workers) as executor:
        for length in range(1, settings.max_length + 1):
            total = len(settings.chars) ** length
            t0 = time.time()
            log.info("Đang kiểm tra độ dài %d (~%s tổ hợp)...", length, f"{total:,}")

            futures = [
                executor.submit(check_prefix, c, length, settings.chars, crypto)
                for c in settings.chars
            ]

            for f in as_completed(futures):
                pwd = f.result()
                if pwd:
                    for remaining in futures:
                        remaining.cancel()
                    return pwd

            elapsed = max(time.time() - t0, 0.001)
            rate_str = f"{total / elapsed:,.0f}"
            log.info(
                "Độ dài %d hoàn tất (%.1fs | ~%s pwd/s). Không tìm thấy.",
                length,
                elapsed,
                rate_str,
            )

    return None
