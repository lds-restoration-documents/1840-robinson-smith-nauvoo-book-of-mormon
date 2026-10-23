# CLAUDE.md

Guidance for Claude Code in this repository.

## What this repo is

A text corpus, not software: AI-assisted transcription of the 1840 third edition of the Book of Mormon (Nauvoo, Ill.: printed by Robinson and Smith, stereotyped by Shepard and Stearns, Cincinnati), from `1840-Book-of-Momron.pdf` (gitignored, 1.5 GB). The PDF has **587 pages**, each one 2320x3062 px photo of an open book (black border, spine, bleed-through), with **no text layer**. Method and tools are adapted from `../1837-pratt-goodson-kirtland-book-of-mormon` (read its `transcription-notes.md` gotchas) and `../1830-grandin-palmyra-book-of-mormon`.

**Status:** transcription complete, proofread and owner-reviewed: all 587 PDF pages have page files; the 569 text pages (7, 9, 11-577) were each re-read against the scan by a second, blind AI agent (9 edits, 2 tie-breaker uses, 20 disagreements), and the owner then decided all 20 disagreements and 41 `uncertain` readings with `tools/make_review_checklist.py` (results in `proofread-disagreements.md`; 32 `uncertain` comments remain by choice, listed in `uncertain-log.md`). Combined files, `printer-typos.md`, `uncertain-log.md` and README are built from the current page files. Not done: any human proofread of the whole text. `check_structure.py` always warns on page 361 (printer's folio 257 for 357). Rebuild with the commands above; never git commit.

## Files
`book-of-mormon-1840-pages/page-NNN.md` (NNN = PDF page, 3 digits) are the source of truth; everything else is derived. Printed folio = PDF page − 4 in the main text. Rebuild (standard library only):
```
python3 tools/compile_markdown.py   # book-of-mormon-1840.md
python3 tools/make_plaintext.py     # book-of-mormon-1840.txt
python3 tools/make_sparse.py        # book-of-mormon-1840-sparse.txt
python3 tools/check_structure.py [--allow-gaps]
```
`tools/prepare_images.py` (needs `~/.venvs/lds-transcribe/bin/python`) crops each PDF page to the text block and writes two native-resolution bands to `work/img/` (gitignored); the crop can clip a running head, so check the full photo before changing a header. `tools/make_review_checklist.py` builds `work/review/checklist.html` (disagreements + uncertain comments, with crops). Rules for transcribers are in `tools/transcription-spec.md`; blind proofreading in `tools/proofread-spec.md`.

## Rules
- Write what the scan shows, never what you think it should say (no corrections from 1830/1837/KJV/memory). Doubtful: `<!-- uncertain: … -->`; unreadable: `[illegible]`.
- Never transcribe without viewing the images. If the image tool fails, stop and report the page.
- Batches of 4 pages per subagent (token economy); skip pages whose file exists; `--clean` each batch's images afterwards.
- Review is lean: local `tesseract` diff to flag pages, blind proofread of flagged pages plus a random sample. Do not claim a page was audited/proofread when it was not; record model and review per range in `transcription-notes.md`.
- No images in tracked files. **Never `git commit` or `git push`**; the owner does. `README.md` is owner-edited: change it with small edits.
