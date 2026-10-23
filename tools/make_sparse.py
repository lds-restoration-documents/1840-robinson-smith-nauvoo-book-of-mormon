#!/usr/bin/env python3
"""Build the sparse plain-text file (Book of Mormon text only) from book-of-mormon-1840.md.

Keeps book titles, chapter headings and paragraphs from the page ranges that hold the
Book of Mormon proper, plus the second title page (PDF page 9, "An account written by the hand
of Mormon upon plates taken from the plates of Nephi ... Moroni"), which was translated from the
plates. Drops everything else: the printed title page with the 1840 imprint (translator, place,
printer, stereotypers, year; not part of that translation), its verso, the testimonies and notices,
and any paragraph that is only an end marker such as FINIS.

The compiled Markdown carries <!-- page NNN --> markers, which this script uses
to decide what is in range. PAGE_RANGES is specific to the scan (PDF page
numbers, not printed folios): see transcription-notes.md §1.

Usage:  python3 tools/make_sparse.py [--md FILE] [--out FILE] [--verbose]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Inclusive PDF-page ranges kept: the second title page (9, translated from the plates) and the text from
# page 11 (1 Nephi) through page 575 (end of Moroni). The title page with the imprint (7), its verso (8)
# and the testimonies (576-577) are outside it. Printed folio = PDF page - 4. Confirmed against the page files.
PAGE_RANGES = [(9, 9), (11, 575)]  # confirmed: 9 second title page, 11 opens 1 Nephi, 575 ends Moroni

END_MARKERS = re.compile(r'\*?(THE END[.,]?|FINIS[.,]?)\*?', re.I)


def in_range(pg):
    return pg is not None and any(a <= pg <= b for a, b in PAGE_RANGES)


def annotate(md_text):
    """Split into paragraphs, each tagged with the image it starts on."""
    page = None
    items = []
    for p in md_text.split('\n\n'):
        ms = re.findall(r'<!-- page (\d+) -->', p)
        clean = re.sub(r'\s*<!-- page \d+ -->\s*', ' ', p).strip()
        if ms and p.startswith('<!-- page'):
            page = int(ms[0])
        if clean:
            items.append((page, clean))
        if ms and not p.startswith('<!-- page'):
            page = int(ms[-1])
    return items


def plain(l):
    l = l.replace('**', '').replace('*', '')
    l = re.sub(r'^#{1,6}[ \t]+', '', l)
    l = re.sub(r'</?[a-zA-Z][^>]*>', '', l)
    return re.sub(r'(?<=\S) {2,}(?=\S)', ' ', l).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1840.md'))
    ap.add_argument('--out', default=str(ROOT / 'book-of-mormon-1840-sparse.txt'))
    ap.add_argument('--verbose', action='store_true', help='list the paragraphs that were dropped')
    args = ap.parse_args()

    if not PAGE_RANGES:
        raise SystemExit('PAGE_RANGES is empty: set the Book of Mormon page ranges at the top of this script first.')

    items = annotate(Path(args.md).read_text(encoding='utf-8'))
    kept, dropped = [], []
    for pg, p in items:
        if in_range(pg) and not END_MARKERS.fullmatch(p.strip()):
            kept.append(p)
        else:
            dropped.append((pg, p))
    text = '\n\n'.join(q for q in (plain(p) for p in kept) if q) + '\n'
    text = re.sub(r'\n{3,}', '\n\n', text)
    Path(args.out).write_text(text, encoding='utf-8')
    print(f'kept {len(kept)} paragraphs, dropped {len(dropped)}, {len(text.split())} words -> {args.out}')
    if args.verbose:
        for pg, p in dropped:
            print(pg, p[:70])


if __name__ == '__main__':
    main()
