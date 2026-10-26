"""Chương trình chính điều phối dò mật khẩu tệp Excel (CLI Entry Point)."""

import logging
import sys
import time

import msoffcrypto.exceptions

from src.config import DEFAULT_SETTINGS, Settings
from src.cracker import phase_bruteforce, phase_wordlist
from src.crypto import extract_crypto_params, save_unlocked, verify_password

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def main(settings: Settings = DEFAULT_SETTINGS) -> str | None:
    """Thực thi toàn bộ quy trình tìm kiếm mật khẩu và mở khóa file."""
    if not settings.file_path.is_file():
        log.error("Không tìm thấy file mục tiêu: %s", settings.file_path)
        sys.exit(1)

    log.info(
        "Excel Password Cracker | %d CPU Cores | File: %s",
        settings.num_workers,
        settings.file_path,
    )

    try:
        crypto = extract_crypto_params(settings.file_path)
    except (ValueError, OSError) as err:
        log.error("Lỗi phân tích file Excel: %s", err)
        sys.exit(1)

    if verify_password("__dummy_wrong_pw__", crypto):
        log.error("Hàm verify_password bị lỗi logic kiểm tra!")
        sys.exit(1)

    t0 = time.time()
    pwd = phase_wordlist(settings.wordlist_path, crypto) or phase_bruteforce(
        crypto, settings
    )
    elapsed = time.time() - t0

    if not pwd:
        log.warning("Không tìm thấy mật khẩu sau %.1f giây.", elapsed)
        return None

    log.info("🎉 TÌM THẤY MẬT KHẨU: '%s' (sau %.1fs)", pwd, elapsed)
    try:
        with settings.result_path.open("a", encoding="utf-8") as f:
            f.write(f"\n[SUCCESS] Password: {pwd}\n")
        save_unlocked(settings.file_path, settings.output_path, pwd)
        log.info(
            "Đã lưu mật khẩu vào '%s' và giải mã file sang '%s'",
            settings.result_path,
            settings.output_path,
        )
    except (ValueError, OSError, msoffcrypto.exceptions.DecryptionError) as err:
        log.error("Lỗi khi lưu kết quả hoặc giải mã file: %s", err)

    return pwd


if __name__ == "__main__":
    main()
