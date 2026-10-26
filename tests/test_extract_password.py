"""Unit tests cho các module trong src/."""

from pathlib import Path

from src.cracker import check_prefix, phase_wordlist
from src.crypto import (
    CryptoParams,
    extract_crypto_params,
    save_unlocked,
    verify_password,
)

SAMPLE_FILE = Path("data/ABMV -  Wet BI formulation.xls")


def test_extract_crypto_params() -> None:
    params = extract_crypto_params(SAMPLE_FILE)
    assert isinstance(params, CryptoParams)
    assert len(params.salt) == 16
    assert len(params.enc_verifier) == 16
    assert len(params.enc_verifier_hash) == 20


def test_verify_password_correct() -> None:
    params = extract_crypto_params(SAMPLE_FILE)
    assert verify_password("12345", params) is True


def test_verify_password_incorrect() -> None:
    params = extract_crypto_params(SAMPLE_FILE)
    assert verify_password("wrong_password", params) is False


def test_save_unlocked(tmp_path: Path) -> None:
    dest_file = tmp_path / "decrypted.xls"
    save_unlocked(SAMPLE_FILE, dest_file, "12345")
    assert dest_file.is_file()
    assert dest_file.stat().st_size > 0


def test_check_prefix() -> None:
    params = extract_crypto_params(SAMPLE_FILE)
    res = check_prefix("1", 5, "0123456789", params)
    assert res == "12345"


def test_phase_wordlist_not_found() -> None:
    params = extract_crypto_params(SAMPLE_FILE)
    non_existent = Path("data/non_existent_wordlist.txt")
    assert phase_wordlist(non_existent, params) is None
