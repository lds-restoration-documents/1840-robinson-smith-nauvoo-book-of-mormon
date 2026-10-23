#!/usr/bin/env python3
"""Cut the scan PDF into the inputs used for transcription.

The PDF (1840-Book-of-Momron.pdf) has one embedded 2320x3062 photo per page, no text layer.
Each photo shows an open book with a black border and the spine, so the paper is found first,
then the printed text block, which is cut into two overlapping horizontal bands.

For each PDF page N this writes, under <out>/img/:
  pNNNN_1_top.jpg      top band (overlaps the bottom band)
  pNNNN_2_bottom.jpg   bottom band
Bands are kept at native resolution (about 1300 px wide, under the 1568 px long edge the image
tool would downscale). With --zoom Z the bands are upscaled by Z and written as pNNNN_*_zZ.jpg;
this adds no information, it only helps the eye on a doubtful spot.

Usage:
  python3 tools/prepare_images.py --pages 21-24
  python3 tools/prepare_images.py --pages 21 --zoom 2 --out work/zoom
  python3 tools/prepare_images.py --pages 21-24 --clean
Requires pypdfium2 and Pillow (~/.venvs/lds-transcribe/bin/python).
"""
import argparse
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / '1840-Book-of-Momron.pdf'
OVERLAP = 0.04  # fraction of text height shared by the two bands
MARGIN = 40     # px around the text block


def parse_pages(spec, total):
    if not spec:
        return list(range(1, total + 1))
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def page_image(page):
    for o in page.get_objects():
        if o.type == 3:
            return o.get_bitmap().to_pil().convert('L')
    raise RuntimeError('no image on page')


def text_box(im):
    """Return (l, t, r, b) of the printed text block inside the photo."""
    w, h = im.size
    small = im.resize((w // 4, h // 4), Image.BILINEAR)
    sw, sh = small.size
    px = small.load()
    # paper = bright; take its bounding columns/rows from row/col means
    cols = [sum(px[x, y] for y in range(sh)) / sh for x in range(sw)]
    paper_cols = [x for x, v in enumerate(cols) if v > 110]
    pl, pr = (paper_cols[0], paper_cols[-1]) if paper_cols else (0, sw - 1)
    prow = [sum(px[x, y] for x in range(pl, pr)) / max(1, pr - pl) for y in range(sh)]
    paper_rows = [y for y, v in enumerate(prow) if v > 110]
    pt, pb = (paper_rows[0], paper_rows[-1]) if paper_rows else (0, sh - 1)
    inset = int(0.04 * (pr - pl))
    xs0, xs1, ys0, ys1 = pl + inset, pr - inset, pt + inset, pb - inset
    # ink positions: use percentiles so page-edge stripes and specks do not widen the box
    dx, dy = [0] * sw, [0] * sh
    for y in range(ys0, ys1):
        for x in range(xs0, xs1):
            if px[x, y] < 100:
                dx[x] += 1
                dy[y] += 1
    def pct(d, lo, hi, q=0.004):
        tot = sum(d)
        if not tot:
            return None
        acc, a, z = 0, lo, hi
        for i in range(lo, hi):
            acc += d[i]
            if acc >= q * tot:
                a = i
                break
        acc = 0
        for i in range(hi - 1, lo - 1, -1):
            acc += d[i]
            if acc >= q * tot:
                z = i
                break
        return a, z
    # horizontal extent: the widest run of inked columns (gaps up to 12 small px bridged), which
    # leaves out the shadowed stack of page edges beside the text
    thr = 0.008 * (ys1 - ys0)
    runs, start, last = [], None, None
    for x in range(xs0, xs1):
        if dx[x] > thr:
            if start is None:
                start = x
            last = x
        elif start is not None and x - last > 20:
            runs.append((last - start, start, last))
            start = None
    if start is not None:
        runs.append((last - start, start, last))
    px_ = max(runs)[1:] if runs else None
    py_ = pct(dy, ys0, ys1)
    if not px_ or not py_:
        return 0, 0, w, h
    ink_cols = list(px_)
    ink_rows = list(py_)
    l, r = ink_cols[0] * 4, ink_cols[-1] * 4
    t, b = ink_rows[0] * 4, ink_rows[-1] * 4
    return max(0, l - MARGIN), max(0, t - MARGIN), min(w, r + MARGIN), min(h, b + MARGIN)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pdf', default=str(PDF))
    ap.add_argument('--out', default=str(ROOT / 'work'))
    ap.add_argument('--pages', help='PDF page numbers, e.g. 1-16,302 (default: all)')
    ap.add_argument('--zoom', type=float, default=1)
    ap.add_argument('--clean', action='store_true', help='delete generated images for --pages and exit')
    args = ap.parse_args()
    out = Path(args.out) / 'img'
    doc = pdfium.PdfDocument(args.pdf)
    pages = parse_pages(args.pages, len(doc))
    if args.clean:
        n = 0
        for p in pages:
            for f in out.glob(f'p{p:04d}_*.jpg'):
                f.unlink()
                n += 1
        print(f'removed {n} files from {out}')
        return
    out.mkdir(parents=True, exist_ok=True)
    suffix = '' if args.zoom == 1 else f'_z{args.zoom:g}'
    for n in pages:
        im = page_image(doc[n - 1])
        l, t, r, b = text_box(im)
        crop = im.crop((l, t, r, b))
        h = crop.height
        pad = h * OVERLAP
        for name, (a, z) in (('1_top', (0, h / 2 + pad)), ('2_bottom', (h / 2 - pad, h))):
            band = crop.crop((0, int(a), crop.width, int(z)))
            if args.zoom != 1:
                band = band.resize((int(band.width * args.zoom), int(band.height * args.zoom)), Image.LANCZOS)
            band.save(out / f'p{n:04d}_{name}{suffix}.jpg', quality=82)
        print(n, (l, t, r, b), crop.size)


if __name__ == '__main__':
    main()
