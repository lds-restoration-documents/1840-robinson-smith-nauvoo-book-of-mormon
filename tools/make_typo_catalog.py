#!/usr/bin/env python3
"""Build printer-typos.md: a catalog of the likely printer's typos and misspellings in the 1840 text.

The list of forms is curated below (triaged from a dictionary scan of the compiled text plus the audit notes); this script
finds every occurrence of each form in book-of-mormon-1840.md, with its image and a snippet of context, so the page
numbers and contexts always come from the current text. Spellings that were normal or intentional for the period or the edition
(shew, sayeth, marvellous, ...) are deliberately NOT cataloged; see the NOT_INCLUDED notes at the end of the output.

Usage:  python3 tools/make_typo_catalog.py [--md FILE] [--out FILE]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (printed, should be, note). `printed` is matched as a whole word, case-sensitive; a tuple (regex, label) matches a pattern.
# Curated from a dictionary scan of the compiled text (words not in /usr/share/dict, then checked by eye) plus a scan for
# doubled words and the "came pass" slip; forms that do not occur in the text simply produce no rows.
SECTIONS = [
    ('Letters dropped, added or wrong (single-word slips)', [
        (w, sh, n) for w, sh, n in [
            ('accordidg', 'according', ''), ('apointed', 'appointed', ''), ('aud', 'and', 'the d for n slip; also worn type'),
            ('bablings', 'babblings', ''), ('brethern', 'brethren', ''), ('brethrea', 'brethren', ''),
            ('cacasses', 'carcasses', ''), ('chall', 'shall', 'damaged type'), ('cilmb', 'climb', ''),
            ('comandments', 'commandments', ''), ('comelinss', 'comeliness', ''), ('contsruct', 'construct', ''),
            ('counfounded', 'confounded', ''), ('couutry', 'country', 'worn n'), ('decendant', 'descendant', ''),
            ('delived', 'delivered', ''), ('dephth', 'depth', ''), ('devlish', 'devilish', ''),
            ('dilligent', 'diligent', ''), ('existance', 'existence', 'period spelling variant'),
            ('fullfil', 'fulfil', ''), ('fullfiled', 'fulfilled', ''), ('gencalogy', 'genealogy', 'worn e'),
            ('geneology', 'genealogy', ''), ('hardnsss', 'hardness', 'damaged type'), ('haugtiness', 'haughtiness', ''),
            ('hearden', 'harden', ''), ('hyprocrite', 'hypocrite', ''), ('idolitary', 'idolatry', ''),
            ('iniqity', 'iniquity', ''), ('inquity', 'iniquity', ''), ('Isarel', 'Israel', ''),
            ('jugdments', 'judgments', ''), ('kngdom', 'kingdom', ''), ('knowedge', 'knowledge', ''),
            ('laciviousness', 'lasciviousness', ''), ('ministed', 'ministered', ''), ('meausure', 'measure', ''),
            ('nnmber', 'number', 'worn u'), ('perservation', 'preservation', ''), ('phophetess', 'prophetess', ''),
            ('plainess', 'plainness', ''), ('pleasin', 'pleasing', ''), ('exeeeding', 'exceeding', 'worn c; owner decision'), ('peopole', 'people', 'split peo-/pole at a line end'), ('poople', 'people', ''), ('chirdren', 'children', 'damaged h; owner decision'),
            ('preceeded', 'preceded', 'period spelling variant'), ('prohet', 'prophet', ''),
            ('secutity', 'security', ''), ('seige', 'siege', 'period spelling variant'), ('spotloss', 'spotless', ''),
            ('strengh', 'strength', ''), ('stubborness', 'stubbornness', ''), ('sufficently', 'sufficiently', ''),
            ('tempations', 'temptations', ''), ('testimoney', 'testimony', ''), ('thay', 'they', ''),
            ('trangressor', 'transgressor', ''), ('vistited', 'visited', ''),
            ('whatsover', 'whatsoever', ''), ('whithsoever', 'whithersoever', ''), ('whosover', 'whosoever', ''),
            ('withersoever', 'whithersoever', ''), ('yearts', 'hearts', 'printed "yearts"'), ('ll', 'all', 'a dropped'),
        ]]),
    ('Words run together or split', [
        ('accordingto', 'according to', 'no space printed'), ('willcome', 'will come', 'no space printed'), ('Godshall', 'God shall', 'no space printed'), ('nochildren', 'no children', 'no space printed; owner decision'),
    ]),
    ('Wrong, missing or doubled words (grammar slips kept as printed)', [
        (('came pass', 'came pass'), 'came to pass', 'the to dropped'),
        (('the the', 'the the'), 'the', 'doubled word'),
        (('of of', 'of of'), 'of', 'doubled word'),
        (('unto unto', 'unto unto'), 'unto', 'doubled word'),
        (('not not', 'not not'), 'not', 'doubled word'),
        (('thou has', 'thou has'), 'thou hast', ''),
        (('had began', 'had began'), 'had begun', ''),
        (('there was but few', 'there was but few'), 'there were but few', ''),
        (('should he preserved', 'should he preserved'), 'should be preserved', 'worn b'),
    ]),
    ('Variant spellings of names (next to a much more frequent spelling)', [
        (w, sh, n) for w, sh, n in [
            ('Almulek', 'Amulek', ''), ('Amalackiah', 'Amalickiah', ''), ('Amalickhiah', 'Amalickiah', ''),
            ('Amalekiah', 'Amalickiah', ''), ('Coriantmr', 'Coriantumr', ''), ('Coriantmur', 'Coriantumr', ''),
            ('Corirantumr', 'Coriantumr', ''), ('Gaddianton', 'Gadianton', ''),
            ('Limhah', 'Limhi', ''), ('Limher', 'Limhi', ''), ('Nepni', 'Nephi', ''), ('Zarahemlah', 'Zarahemla', ''),
            ('Zerahemla', 'Zarahemla', ''), ('Ammonihahits', 'Ammonihahites', ''),
        ]]),
]

# Misspellings that recur (the same slip printed several times): listed in their own section, with all pages.
RECURRING = [
    ('harrass', ['harrass'], 'harass', 'single r/ss'),
    ('brethern/brethrea', ['brethern', 'brethrea'], 'brethren', 'wrong letter before the end'),
    ('aud', ['aud'], 'and', 'worn d/n slip'),
    ('had began', ['had began'], 'had begun', 'wrong participle'),
]

NOT_INCLUDED = """## Not included: spellings that were normal or intentional

Spellings that were normal or intentional for the period or the edition are not printer's slips and are left out: `shew`/`shewed`/`shewn`/`sheweth`/`shewing`, `annointed`, `burthen(s)`/`burthensome`, `centre`, `sepulchre`, `vapour`, `armour`, `lustre`, `mouldering`, `moulten`, `favour`, `offence`, `skilful`, `wilfully`/`wilfulness`, `marvellous`, `quarrellings`, `counsellor(s)`, `cimeter(s)`/`cymeter`, `carcases`, `phrensied`, `wrapt`, `threatnings`, `dissentions`, `dependant`, `changable`, `fulfil`, `spake`, `whoso`, `stiffneckedness`, `abridgement`, `ancles`, and the archaic verb endings (`-eth`, `-est`). Roman-numeral chapter numbers (`ii`, `xix`) and place and personal names are also left out unless a variant sits next to a much more frequent spelling of the same name (see the names section).
"""


def load(md):
    raw = md.read_text(encoding='utf-8')
    parts = re.split(r'<!-- page (\d+) -->', raw)
    segs, cur = [], 0
    for i, t in enumerate(parts):
        if i % 2 == 1:
            cur = int(t)
            continue
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        segs.append((cur, re.sub(r'\s+', ' ', t)))
    return segs


def find(segs, spec):
    """Yield (page, snippet) for each occurrence."""
    if isinstance(spec, tuple):
        pat, hit = spec
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(pat) + r'(?![A-Za-z])')
        hl = hit
    else:
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(spec) + r'(?![A-Za-z])')
        hl = spec
    for pg, t in segs:
        if pg < 1 or pg > 587:
            continue
        for m in rx.finditer(t):
            a = max(0, m.start() - 38)
            b = min(len(t), m.end() + 30)
            s = t[a:b]
            i = s.find(hl) if hl in s else 0
            s = s[:i] + '**' + s[i:i + len(hl)] + '**' + s[i + len(hl):]
            yield pg, ('…' if a else '') + s.strip() + ('…' if b < len(t) else '')


def printed(pg):
    return str(pg - 4) if 11 <= pg <= 577 else '—'  # printed folio = PDF page - 4 (page 11 is p. 7)


def row(spec, should, note, segs):
    out = []
    for pg, snip in find(segs, spec):
        label = spec[1] if isinstance(spec, tuple) else spec
        out.append((pg, '| `%s` | %s | %d | %s | %s%s |' % (label, should, pg, printed(pg), snip.replace('|', '\\|'),
                                                           (' (' + note + ')') if note else '')))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1840.md'))
    ap.add_argument('--out', default=str(ROOT / 'printer-typos.md'))
    args = ap.parse_args()
    segs = load(Path(args.md))
    out, total, missing = [], 0, []
    header = '| Printed | Should be | Image | Printed p. | In context |\n|---|---|---|---|---|'
    body = []
    for title, items in SECTIONS:
        rows = []
        for spec, should, note in items:
            r = row(spec, should, note, segs)
            if not r:
                missing.append(spec)
            rows += r
        rows.sort(key=lambda x: x[0])
        total += len(rows)
        body.append('\n## %s (%d)\n\n%s\n%s' % (title, len(rows), header, '\n'.join(r for _, r in rows)))
    rec = []
    for label, forms, should, why in RECURRING:
        hits = [h for f in forms for h in find(segs, f)]
        hits.sort()
        total += len(hits)
        pages = ', '.join(str(p) for p, _ in hits)
        rec.append('| `%s` | %s | %d | %s | %s |' % (label, should, len(hits), why, pages))
    intro = f"""# Printer's typos and misspellings in the 1840 Book of Mormon

A catalog of the places where the 1840 print itself has a slip of the type, a misspelling, or a doubled word, as the transcription records
it. {total} occurrences, grouped by the kind of slip, each with its image, printed page (PDF page - 4 in the text) and context.

**What is and is not here.** The transcription keeps every printed error exactly as printed (nothing was corrected from later editions), so
all of these are in the page files as printed. This list leaves out spellings that were normal or intentional for the period or the edition
(`shew`, `sayeth`, `marvellous`, `wilfully` and the like; see the end of the file). It was built from a dictionary scan of the whole text,
triaged by hand, so it is **likely, not exhaustive**: a slip that happens to produce another real word (`he` for `be`) is only caught where it was noticed, and a few
entries are judgment calls (marked in the notes). Some rows are worn-type readings (`chall`, `chirdren`): the scan shows a letter that looks like the printed one, which the
audits kept as printed. Names are listed only where a variant sits next to a much more frequent spelling of the same name; whether such a variant is a typo or a deliberate spelling is not always certain.

**Where to see the original.** Numbers are PDF page numbers of the scan 1840-Book-of-Momron.pdf (587 JPGs, numbered 001-587 in order; printed page = PDF page - 4 in the main text). No images are included in this repository.

Generated by `tools/make_typo_catalog.py` from the live text, so page numbers and contexts stay current if the pages are edited.
"""
    recsec = '\n## Misspellings that recur\n\nThe same slip printed more than once (compositor habits rather than one-off slips).\n\n| Printed | Should be | Times | Slip | images |\n|---|---|---|---|---|\n' + '\n'.join(rec)
    Path(args.out).write_text(intro + '\n'.join(body) + '\n' + recsec + '\n\n' + NOT_INCLUDED, encoding='utf-8')
    print(f'{total} occurrences -> {args.out}')
    if missing:
        print('NOT FOUND in the text:', missing)


if __name__ == '__main__':
    main()
