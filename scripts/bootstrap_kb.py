#!/usr/bin/env python3
"""
Bootstrap knowledge base assets by downloading from URLs defined in kb_assets_manifest.json.
- Preserves local files if present and matching optional SHA-256
- Creates directories as needed
- Prints clear progress and failures
"""
from __future__ import annotations

import json
import sys
import hashlib
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

CHUNK_SIZE_BYTES = 1024 * 1024


def compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE_BYTES), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def stream_download(url: str, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url) as response, destination_path.open("wb") as out:
        while True:
            chunk = response.read(CHUNK_SIZE_BYTES)
            if not chunk:
                break
            out.write(chunk)


def main() -> int:
    manifest_path = Path("kb_assets_manifest.json")
    if not manifest_path.exists():
        print("kb_assets_manifest.json not found in project root.", file=sys.stderr)
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in kb_assets_manifest.json: {e}", file=sys.stderr)
        return 1

    if not isinstance(manifest, dict):
        print("Manifest JSON must be an object mapping local paths to {url, sha256?}.", file=sys.stderr)
        return 1

    any_downloaded = False
    for rel_path, meta in manifest.items():
        if not isinstance(meta, dict) or "url" not in meta:
            print(f"Skipping {rel_path}: missing 'url' field.", file=sys.stderr)
            continue

        url = meta["url"]
        expected_sha = meta.get("sha256")
        dest = Path(rel_path)

        if dest.exists():
            if expected_sha:
                actual_sha = compute_sha256(dest)
                if actual_sha == expected_sha:
                    print(f"OK (exists): {rel_path}")
                    continue
                else:
                    print(f"Checksum mismatch for {rel_path}; re-downloading…")
                    try:
                        dest.unlink()
                    except FileNotFoundError:
                        pass
            else:
                print(f"Exists (no checksum provided): {rel_path}")
                continue

        print(f"Downloading {rel_path} from {url} …")
        try:
            stream_download(url, dest)
            any_downloaded = True
        except (URLError, HTTPError) as e:
            print(f"Failed to download {url}: {e}", file=sys.stderr)
            return 2

        if expected_sha:
            actual_sha = compute_sha256(dest)
            if actual_sha != expected_sha:
                print(f"Checksum FAILED for {rel_path}", file=sys.stderr)
                return 3
            print(f"Checksum OK: {rel_path}")

    print("Asset bootstrap complete." if any_downloaded else "All assets already present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


