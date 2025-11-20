# core/mhd_descent.py
# Sovariel — Monadic Harmonic Descent (MHD v5.1)
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# 64-step recursive SHA-256 descent starting from an arbitrary scalar.
# Designed for cryptographic puzzle hunting and entropy exploration.
# Uses secp256k1 public key derivation and Bitcoin address matching.

from __future__ import annotations

import hashlib
from typing import List, Dict, Optional

import ecdsa
from ecdsa import SigningKey, SECP256k1
from ecdsa.ellipticcurve import Point

# Bitcoin address tools
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_encode(data: bytes) -> str:
    """Encode bytes to Base58 (Bitcoin-style)."""
    n = int.from_bytes(data, "big")
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(BASE58_ALPHABET[r])
    # Leading zeros
    leading_zeros = len(data) - len(data.lstrip(b"\x00"))
    return BASE58_ALPHABET[0] * leading_zeros + "".join(res[::-1])


def hash160(data: bytes) -> bytes:
    """SHA-256 followed by RIPEMD-160."""
    sha = hashlib.sha256(data).digest()
    ripemd = hashlib.new("ripemd160", sha)
    return ripemd.digest()


def public_key_to_address(pubkey_bytes: bytes, compressed: bool = True) -> str:
    """Convert compressed/uncompressed public key to legacy Bitcoin address."""
    if compressed and pubkey_bytes[0] not in {2, 3}:
        raise ValueError("Invalid compressed public key")
    h160 = hash160(pubkey_bytes)
    payload = b"\x00" + h160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest())[:4]
    return base58_encode(payload + checksum)


def private_key_to_wif(private_key_bytes: bytes, compressed: bool = True) -> str:
    """Convert 32-byte private key to Wallet Import Format."""
    payload = b"\x80" + private_key_bytes
    if compressed:
        payload += b"\x01"
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58_encode(payload + checksum)


def derive_public_key(private_key_bytes: bytes, compressed: bool = True) -> bytes:
    """Derive compressed or uncompressed public key from 32-byte private key."""
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    prefix = b"\x02" if compressed and y % 2 == 0 else b"\x03" if compressed else b"\x04"
    if compressed:
        return prefix + x.to_bytes(32, "big")
    return prefix + x.to_bytes(32, "big") + y.to_bytes(32, "big")


def monadic_harmonic_descent(
    start_scalar_hex: str,
    steps: int = 64,
    target_addresses: Optional[set[str]] = None,
) -> List[Dict[str, str | bool]]:
    """
    Perform chained SHA-256 descent from a starting scalar.

    Parameters
    ----------
    start_scalar_hex : str
        64-character hex string (or shorter — will be left-padded)
    steps : int
        Number of descent iterations (default 64)
    target_addresses : set[str] | None
        Optional set of Bitcoin addresses to watch for collision

    Returns
    -------
    log : list[dict]
        Full ancestry log with keys, addresses, and match flags
    """
    if target_addresses is None:
        target_addresses = set()

    scalar_bytes = bytes.fromhex(start_scalar_hex.zfill(64))
    log: List[Dict[str, str | bool]] = []

    for depth in range(steps):
        priv_key = scalar_bytes[:32]

        pub_compressed = derive_public_key(priv_key, compressed=True)
        pub_uncompressed = derive_public_key(priv_key, compressed=False)

        addr_compressed = public_key_to_address(pub_compressed, compressed=True)
        addr_uncompressed = public_key_to_address(pub_uncompressed, compressed=False)

        wif_compressed = private_key_to_wif(priv_key, compressed=True)
        wif_uncompressed = private_key_to_wif(priv_key, compressed=False)

        match_c = addr_compressed in target_addresses
        match_u = addr_uncompressed in target_addresses

        log.append(
            {
                "depth": depth,
                "private_hex": priv_key.hex(),
                "address_compressed": addr_compressed,
                "address_uncompressed": addr_uncompressed,
                "wif_compressed": wif_compressed,
                "wif_uncompressed": wif_uncompressed,
                "match": match_c or match_u,
            }
        )

        if match_c or match_u:
            print(f"Collision found at depth {depth}")
            break

        # Next scalar = SHA-256(current private key)
        scalar_bytes = hashlib.sha256(priv_key).digest()

    return log


# === DEMO ===
if __name__ == "__main__":
    # Example with no targets — just explores the chain
    ancestry = monadic_harmonic_descent("c07156d7829ae8f3")

    for entry in ancestry[:5]:  # show first 5 steps
        print(f"Depth {entry['depth']:02d} → {entry['address_compressed']}")
    print(f"Explored {len(ancestry)} steps")
