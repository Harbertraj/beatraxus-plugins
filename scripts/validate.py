#!/usr/bin/env python3
"""Validate repository.json and plugins/*.json against BeatRaxus schema v1."""
import json, re, sys
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"^[A-Za-z0-9_]{1,64}$")
VER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
CATS = {"music_source", "metadata", "lyrics", "artwork", "playlist", "scrobbling", "video_source"}
errors = []

def err(msg): errors.append(msg)

index_path = ROOT / "repository.json"
if index_path.stat().st_size > 512 * 1024: err("repository.json exceeds 512 KiB")
index = json.loads(index_path.read_text("utf-8"))
if index.get("schemaVersion") != 1: err("index schemaVersion must be 1")
if not str(index.get("name", "")).strip(): err("index name required")
plugins = index.get("plugins", [])
if len(plugins) > 100: err("more than 100 plugins")
ids = [p.get("id") for p in plugins]
if len(set(ids)) != len(ids): err("duplicate plugin ids")

for p in plugins:
    pid = p.get("id", "?")
    if not ID.match(str(p.get("id", ""))): err(f"{pid}: invalid id")
    if not VER.match(str(p.get("version", ""))): err(f"{pid}: invalid version")
    if p.get("category") not in CATS: err(f"{pid}: invalid category")
    if not ID.match(str(p.get("adapterId", ""))): err(f"{pid}: invalid adapterId")
    url = str(p.get("manifestUrl", ""))
    if "://" in url:
        u = urlparse(url)
        if u.scheme != "https" or not u.hostname or u.username or u.password:
            err(f"{pid}: manifestUrl must be HTTPS without credentials")
        continue
    mp = (ROOT / url).resolve()
    if ROOT not in mp.parents or not mp.is_file():
        err(f"{pid}: manifest not found: {url}"); continue
    if mp.stat().st_size > 128 * 1024: err(f"{pid}: manifest exceeds 128 KiB")
    m = json.loads(mp.read_text("utf-8"))
    if m.get("schemaVersion") != 1: err(f"{pid}: manifest schemaVersion must be 1")
    for k in ("id", "version", "category", "adapterId"):
        if m.get(k) != p.get(k): err(f"{pid}: manifest {k} != index {k}")
    cfg = m.get("configuration", {})
    if len(json.dumps(cfg).encode()) > 32 * 1024: err(f"{pid}: configuration exceeds 32 KiB")
    if int(m.get("minAppVersionCode", 0)) < 0: err(f"{pid}: bad minAppVersionCode")

if errors:
    print("\n".join("ERROR: " + e for e in errors)); sys.exit(1)
print(f"OK: {len(plugins)} plugins valid")
