"""Module xử lý mã hóa và phân tích cấu trúc tệp Excel XLS qua msoffcrypto."""

import struct
from dataclasses import dataclass
from pathlib import Path

import olefile
from msoffcrypto import OfficeFile
from msoffcrypto.method.rc4_cryptoapi import DocumentRC4CryptoAPI


@dataclass(frozen=True, slots=True)
class CryptoParams:
    """Tham số mã hóa trích xuất từ FilePass record của OLE workbook."""

    salt: bytes
    enc_verifier: bytes
    enc_verifier_hash: bytes


def verify_password(password: str, crypto: CryptoParams) -> bool:
    """Xác thực mật khẩu qua thư viện msoffcrypto DocumentRC4CryptoAPI."""
    return DocumentRC4CryptoAPI.verifypw(
        password=password,
        salt=crypto.salt,
        keySize=128,
        encryptedVerifier=crypto.enc_verifier,
        encryptedVerifierHash=crypto.enc_verifier_hash,
    )


def extract_crypto_params(file_path: Path) -> CryptoParams:
    """Đọc thông tin mã hóa từ FilePass record trong OLE XLS file."""
    with (
        olefile.OleFileIO(file_path) as ole,
        ole.openstream("Workbook") as stream,
    ):
        wb = stream.read()

    i = 0
    while i < len(wb) - 4:
        rt, rl = struct.unpack_from("<HH", wb, i)
        if rt == 0x002F:  # FilePass record
            data = wb[i + 4 : i + 4 + rl]
            major = struct.unpack_from("<H", data, 2)[0]
            match major:
                case 4:  # RC4 CryptoAPI
                    rest = data[6:]
                    hdr_size = struct.unpack_from("<I", rest, 4)[0]
                    vs = 8 + hdr_size
                    return CryptoParams(
                        salt=rest[vs + 4 : vs + 20],
                        enc_verifier=rest[vs + 20 : vs + 36],
                        enc_verifier_hash=rest[vs + 40 : vs + 60],
                    )
                case _:
                    raise ValueError(
                        f"Unsupported encryption major version: {major} in FilePass record"
                    )
        i += 4 + rl
    raise ValueError("Không tìm thấy FilePass record trong file Excel.")


def save_unlocked(file_path: Path, output_path: Path, pwd: str) -> None:
    """Giải mã file Excel và lưu sang đường dẫn output."""
    with file_path.open("rb") as f:
        office_file = OfficeFile(f)
        office_file.load_key(password=pwd)
        with output_path.open("wb") as out:
            office_file.decrypt(out)
