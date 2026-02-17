
from auth import get_password_hash
import sys

DEFAULT_PASS = "medellin2026"

try:
    print(f"Hashing '{DEFAULT_PASS}' (len={len(DEFAULT_PASS)})")
    h = get_password_hash(DEFAULT_PASS)
    print(f"Hash: {h}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
