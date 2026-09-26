#!/usr/bin/env python3
"""Serve the orderbook page locally and open it in the default browser."""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import re
import socket
import threading
import webbrowser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
PAGE = "orderbook_demo_three_products.html"
DATA_ROOT = ROOT / "data"


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/datasets":
            payload = json.dumps(
                {"datasets": scan_datasets()},
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def product_name(filename: str) -> str:
    stem = Path(filename).stem.strip()
    return stem.split("-", 1)[0] or stem


def product_key(filename: str) -> str:
    name = product_name(filename)
    prefix_match = re.match(r"[A-Za-z]+", name)
    if prefix_match:
        return prefix_match.group(0).upper()
    safe_name = re.sub(r"[^0-9A-Za-z_]+", "_", name).strip("_")
    return safe_name or Path(filename).stem


def scan_datasets() -> dict[str, dict[str, dict[str, str]]]:
    datasets: dict[str, dict[str, dict[str, str]]] = {}
    if not DATA_ROOT.is_dir():
        return datasets

    for md_path in sorted(DATA_ROOT.glob("*/*/*/md/*.feather")):
        try:
            year, month, day, folder, filename = md_path.relative_to(DATA_ROOT).parts
            date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
        except (ValueError, TypeError):
            continue
        if folder != "md":
            continue

        key = product_key(filename)
        trade_path = md_path.parent.parent / "trade" / filename
        if not trade_path.is_file():
            continue
        date_products = datasets.setdefault(date, {})
        name = product_name(filename)
        if key in date_products and date_products[key]["file"].lower() != filename.lower():
            key = name
        while key in date_products and date_products[key]["file"].lower() != filename.lower():
            key = f"{name}_{len(date_products) + 1}"
        date_products[key] = {
            "key": key,
            "name": name,
            "file": filename,
            "mdFile": filename,
            "tradeFile": filename,
        }

    return dict(sorted(datasets.items()))


def available_port(preferred: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind(("127.0.0.1", preferred))
        except OSError:
            probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the orderbook viewer.")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    port = available_port(args.port)
    handler = functools.partial(NoCacheHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{port}/{PAGE}"

    print(f"Orderbook server: {url}")
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.4, webbrowser.open, args=(url,)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
