"""Cấu hình mặc định cho hệ thống dò mật khẩu Excel."""

import multiprocessing as mp
import string
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Cấu hình đường dẫn và thông số cho quá trình quét."""

    file_path: Path = Path("data/ABMV -  Wet BI formulation.xls")
    output_path: Path = Path("data/unlocked_ABMV.xls")
    wordlist_path: Path = Path("data/wordlist.txt")
    result_path: Path = Path("secrets/found_password.txt")
    max_length: int = 6
    num_workers: int = mp.cpu_count()
    chars: str = (
        string.digits
        + string.ascii_lowercase
        + string.ascii_uppercase
        + string.punctuation
    )


DEFAULT_SETTINGS = Settings()
