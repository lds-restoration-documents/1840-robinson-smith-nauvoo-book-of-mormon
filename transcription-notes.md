# Transcription notes — 1840 Robinson & Smith Nauvoo Book of Mormon

## 1. Source and layout (survey, PDF page numbers)
- Source: `1840-Book-of-Momron.pdf`, 587 pages, photos of a copy from the Historian's Office Library (Church of Jesus Christ of Latter-day Saints), with handwritten notes and stamps. No text layer. The images come from the Joseph Smith Papers (https://www.josephsmithpapers.org/paper-summary/book-of-mormon-1840/), downloaded with Archive Viewer (https://archiveviewer.org) and printed to this PDF.
- 1 front cover; 2 inside cover label; 3–4 handwritten inscription/notes; 5–6 blank leaves with title bleed-through; **7 title page** ("THE BOOK OF MORMON … Translated by Joseph Smith, Jr. THIRD EDITION, carefully revised by the translator. NAUVOO, ILL.: Printed by Robinson and Smith. Stereotyped by Shepard and Stearns, Cincinnati, Ohio. 1840."); 8 verso (copyright notice, 1829); 9 further title/leaf (check); 10 blank; **11 opens 1 Nephi (printed p. 7)**.
- **Printed folio = PDF page − 4** in the main text (12 = p. 8, 21 = p. 17, 300 = p. 296, 575 = p. 571).
- **Book openings (PDF page, as transcribed; printed folio = page − 4):** 1 Nephi 11 (p. 7); 2 Nephi 63 (mid-page, p. 59); Jacob 125 (mid-page); Enos 144 (mid-page); Jarom 147 (mid-page, under an Enos running head); Omni 149; Words of Mormon 152 (mid-page); Mosiah 154 (mid-page); Alma 220; Helaman 400 (mid-page); "The Prophecy of Nephi, the son of Helaman" (chapter III of Helaman) 419; Third Nephi, "The Book of Nephi, the son of Nephi" 443 (mid-page); Fourth Nephi, "The Book of Nephi, who is the son of Nephi, one of the disciples of Jesus Christ" 503; "Book of Mormon" 508; Ether 527 (mid-page); Moroni 561. Moroni ends with "Amen." on 575 (p. 571). 576 Testimony of the Three Witnesses (HISTORIAN'S OFFICE stamp across the top); 577 Testimony of the Eight Witnesses; 578–585 blank leaves; 586 back cover; 587 spine. Page 9 is a second title page ("THE BOOK OF MORMON. AN ACCOUNT WRITTEN BY THE HAND OF MORMON … MORONI."), page 7 the title page, page 8 its verso (copyright notice).
- Sparse text range (`tools/make_sparse.py`): page 7 (title page, imprint dropped) and pages 11–575; page 9, the testimonies (576–577) and the placeholders are outside it. Confirmed against the page files.
- Pages 1–6, 10 and 578–587 have placeholder files (descriptions only); handwriting and library labels are not transcribed.
- Header OCR of all pages: `work/survey/headers.txt` (local, gitignored).

## 2. Conventions
See `tools/transcription-spec.md`.

## 3. Review log
| PDF pages | Written by | Reviewed by | Notes |
|---|---|---|---|
| 7, 8, 9, 11 | Sonnet 5.5, main session (pilot) | none | title page, verso, second title page, opening of 1 Nephi |
| 12–577 | Sonnet 5.5 subagents, 4 pages each (576–577 two pages) | `check_structure.py`; blind proofread of every text page (next row) | every agent viewed both bands of every page |
| all 569 text pages (PDF 7, 9, 11–577): 70 flagged by the OCR comparison, a 60-page random sample (seed 1840), then the other 439 | none (blind) | blind Sonnet 5.5 subagent proofread, 4 pages per agent, own bands per agent | 9 edits (pages 63, 126, 182, 215, 243, 295, 325, 406, 468) and 2 tie-breaker uses (386 kept a comma; 531 comma changed to period), 20 logged disagreements, all listed in `proofread-disagreements.md` and since decided by the owner (see below); the first 130 pages (flagged + sample) needed 4 edits, the sample 1 in 60 pages |
| 1–6, 10, 578–587 | main session | none | description-only placeholders from thumbnails |

Doubtful readings rechecked at 3x zoom in the main session: page 159 folio, "Sidon" on 508, and 27 flagged readings (12 settled; see `CLAUDE.md` and `uncertain-log.md` for what remains). The review pass: `tools/ocr_diff.py` compared a local tesseract OCR of every text page with its page file (character level, runs of 4 or more differing characters); the 70 pages with a difference rate of 1% or more were proofread first, then a random 12% of the rest (60) as a calibration sample (1 edit in 60 pages), then, at the owner's request, all remaining pages. Every one of the 569 text pages has now been read against the scan by a second, blind agent. The non-text pages (1–6, 8, 10, 578–587) are descriptions only and were not proofread. No page has been proofread by a person, and the second reader is itself an AI with the same blind spots on worn type, so the open `uncertain` marks and the disagreements still need a human look at the scan.

## Owner review (2026-10-23)
The owner worked through `work/review/checklist.html` (built by `tools/make_review_checklist.py` from `proofread-disagreements.md` and the `uncertain` comments): the 20 proofread disagreements and 41 uncertain readings, each against a crop of the scan. Outcomes are in `proofread-disagreements.md` ("Resolved by the owner"): 7 disagreements and 7 uncertain readings changed the page files (69, 220, 407, 457, 472, 538, 548; 91, 107, 179, 184, 365, 379, 527; page 218's head, "CHAPTER XI." on 105 and the comma on 386 were confirmed as they were), the rest were kept. Page 198 keeps its cut-off "de-" hyphen. Page 361's head prints "257" for 357 (printer error, now commented). Still unproofread by a person: everything else. 32 `uncertain` comments remain by choice.

**Gotcha:** `prepare_images.py` crops to the ink block and can clip a running head (218: the proofreader saw only a partly cut "214" and the file was right). Check the full photo before changing a header; the whole page is `page_image(doc[n-1])` in that script.
