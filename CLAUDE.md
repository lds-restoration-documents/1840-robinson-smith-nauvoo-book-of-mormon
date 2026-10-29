# CLAUDE.md

Guidance for Claude Code in this repository.

## What this repo is

A text corpus, not software: AI-assisted transcription of the 1840 third edition of the Book of Mormon (Nauvoo, Ill.: printed by Robinson and Smith, stereotyped by Shepard and Stearns, Cincinnati), from `1840-Book-of-Momron.pdf` (gitignored, 1.5 GB). The PDF has **587 pages**, each one 2320x3062 px photo of an open book (black border, spine, bleed-through), with **no text layer**. Method and tools are adapted from `../1837-pratt-goodson-kirtland-book-of-mormon` (read its `transcription-notes.md` gotchas) and `../1830-grandin-palmyra-book-of-mormon`.

**Status:** transcription complete, proofread and owner-reviewed: all 587 PDF pages have page files; the 569 text pages (7, 9, 11-577) were each re-read against the scan by a second, blind AI agent (9 edits, 2 tie-breaker uses, 20 disagreements), and the owner then decided all 20 disagreements and 41 `uncertain` readings with `tools/make_review_checklist.py` (results in `proofread-disagreements.md`; 32 `uncertain` comments remain by choice, listed in `uncertain-log.md`). Combined files, `printer-typos.md`, `uncertain-log.md` and README are built from the current page files. Not done: any human proofread of the whole text. `check_structure.py` always warns on page 361 (printer's folio 257 for 357). Rebuild with the commands above; never git commit.
A second blind proofread of 50 random pages (seed 1841) is also done: 2 edits (105, 171), and 2 disagreements awaiting the owner (136 blot between "tree" and "profiteth"; 427 "whatsoeverye" spacing); see `proofread-disagreements.md`. A third blind round of 25 pages (seed 1842) found 1 edit (299) and no disagreements. The owner then had every page second-read: the second blind pass is now complete for all text pages (7, 9, 11-577; seed rounds plus a sequential pass), with 6 edits in total (105, 135, 171, 299, 380, 492). The owner decided the last six open items (2026-10-29): one edit (135, "all the the land"), the rest kept as in the file (97, 136, 313, 427, 472); see `proofread-disagreements.md`. To run another round, give each agent 4 pages (`prepare_images.py --pages a,b,c,d --out work/proof2-X`), tell it to follow `tools/proofread-spec.md`, log to `work/proof2-log-<first page>.md`, and do not delete those logs. Then rebuild, and record edits and disagreements in `proofread-disagreements.md` and `transcription-notes.md` §3.

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
