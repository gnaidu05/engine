#!/usr/bin/env python3
"""Rebuild the NIRF directory embedded in index.html from nirfindia.org.

Downloads the official NIRF *Engineering* ranking pages for 2023-2025 —
ranks 1-100 plus the 101-150 / 151-200 / 201-300 rank-band pages — merges
them by institute, and rewrites the block between NIRF_DIRECTORY_START /
NIRF_DIRECTORY_END markers in index.html.

Run from the repo root:  python3 scripts/build_nirf_directory.py
(needs: requests, beautifulsoup4)
"""
import datetime
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

YEARS = [2025, 2024, 2023]
PAGES = [  # (suffix, rank value: None = read from the Rank column, else the band label)
    ("EngineeringRanking.html", None),
    ("EngineeringRanking150.html", "101-150"),
    ("EngineeringRanking200.html", "151-200"),
    ("EngineeringRanking300.html", "201-300"),
]
UA = {"User-Agent": "Mozilla/5.0 (college-priority-dashboard NIRF directory builder)"}


def clean_name(td):
    a = td.find("a")
    text = a.get_text(" ", strip=True) if a else td.get_text(" ", strip=True)
    text = re.split(r"More Details", text)[0]
    return re.sub(r"\s+", " ", text).strip()


def parse_page(html, band):
    """Yield (name, city, state, rank) rows from a ranking page."""
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td", recursive=False)
        if len(tds) < 4:
            continue
        first = tds[0].get_text(" ", strip=True)
        if not re.match(r"^IR-", first):  # institute IDs look like IR-E-U-0456
            continue
        name = clean_name(tds[1])
        city = tds[2].get_text(" ", strip=True)
        state = tds[3].get_text(" ", strip=True)
        if band is not None:
            rank = band
        else:
            rank_txt = tds[-1].get_text(" ", strip=True)
            m = re.search(r"\d+", rank_txt)
            if not m:
                continue
            rank = int(m.group())
        if name:
            out.append((name, city, state, rank))
    return out


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s.lower())).strip()


def main():
    merged = {}  # key -> entry
    counts = {}
    for year in YEARS:
        year_rows = 0
        for suffix, band in PAGES:
            url = f"https://www.nirfindia.org/Rankings/{year}/{suffix}"
            try:
                resp = requests.get(url, headers=UA, timeout=60)
            except requests.RequestException as exc:
                print(f"  {url} -> ERROR {exc}")
                continue
            if resp.status_code != 200:
                print(f"  {url} -> HTTP {resp.status_code} (skipped)")
                continue
            rows = parse_page(resp.text, band)
            print(f"  {url} -> {len(rows)} rows")
            year_rows += len(rows)
            for name, city, state, rank in rows:
                key = norm(name) + "|" + norm(city)
                e = merged.setdefault(key, {"n": name, "c": city, "s": state,
                                            "r25": None, "r24": None, "r23": None})
                e[f"r{year % 100}"] = rank
        counts[year] = year_rows
        if year_rows < 250:
            print(f"SANITY FAIL: only {year_rows} rows parsed for {year} (expected ~300)")
            sys.exit(1)

    entries = sorted(merged.values(), key=lambda e: norm(e["n"]))
    print(f"merged institutes: {len(entries)}")

    with open("index.html", encoding="utf-8") as f:
        src = f.read()
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    stamp = datetime.date.today().isoformat()
    src = re.sub(
        r"/\* NIRF_DIRECTORY_START \*/[\s\S]*?/\* NIRF_DIRECTORY_END \*/",
        f"/* NIRF_DIRECTORY_START */\nconst NIRF_DIRECTORY = {payload};\n/* NIRF_DIRECTORY_END */",
        src, count=1)
    src = re.sub(
        r"/\* NIRF_DIRECTORY_META_START \*/[\s\S]*?/\* NIRF_DIRECTORY_META_END \*/",
        f'/* NIRF_DIRECTORY_META_START */\nconst NIRF_META = "official nirfindia.org engineering rankings, fetched {stamp}";\n/* NIRF_DIRECTORY_META_END */',
        src, count=1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(src)
    print(f"index.html updated ({stamp}); per-year rows: {counts}")


if __name__ == "__main__":
    main()
