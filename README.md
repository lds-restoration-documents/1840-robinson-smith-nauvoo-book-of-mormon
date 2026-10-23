# 1840 Robinson & Smith Nauvoo Book of Mormon
[Markdown](#what-is-markdown) & Plain Text extractions of the content of the 1840 (third) edition of the Book of Mormon, printed at Nauvoo, Illinois, by Robinson and Smith and stereotyped by Shepard and Stearns of Cincinnati. Extracted using AI.

## Files
* [book-of-mormon-1840.md](book-of-mormon-1840.md): the whole text in a single [Markdown](#what-is-markdown) file (about 270,000 words): the title pages, the Book of Mormon and the testimonies of the Three and Eight Witnesses. A `<!-- page NNN -->` comment marks where each PDF page begins.
* [book-of-mormon-1840.txt](book-of-mormon-1840.txt): the same text as plain text, with no [Markdown](#what-is-markdown).
* [book-of-mormon-1840-sparse.txt](book-of-mormon-1840-sparse.txt): plain text of the Book of Mormon proper only: the title page (without its imprint) and the text from 1 Nephi through Moroni, leaving out the copyright notice, the second title page and the testimonies of the witnesses.
* [book-of-mormon-1840-pages/](book-of-mormon-1840-pages/): one [Markdown](#what-is-markdown) file per page of the scan PDF (`page-001.md` to `page-587.md`). File numbers are PDF page numbers (printed page number = PDF page minus 4 in the main text). These are the source of truth; the files above are generated from them. Pages with no text (covers, labels, blank leaves) have a one-line description.
* [printer-typos.md](printer-typos.md): a catalog of the printer's slips and misspellings in the 1840 print (about 125 occurrences, each with its page and context), leaving out spellings that were normal or intentional for the period, such as "shew" (likely, not exhaustive).

## What is in the 1840 edition
* This is the **third edition**, "carefully revised by the translator", printed at Nauvoo, Illinois, by Robinson and Smith, stereotyped by Shepard and Stearns of Cincinnati, Ohio, 1840.
* **No verse numbers**, no double columns, no footnotes and no cross-references; text in paragraphs on a single wide column. Chapters are numbered within each book in Roman numerals, with an ornament printed between chapters.
* Spelling, capitalization, punctuation and grammar are kept exactly as printed, **printer's errors included**; nothing has been corrected from other editions. Punctuation is **ordinary** (commas, semicolons, colons and periods), much fuller than the sparse punctuation of the 1830 first edition. Printed page numbers and running heads are kept too, including the odd one (the head on PDF page 361 prints 257 for 357).
* Like the 1830 and 1837 editions, it has **no later book divisions** (no 3 Nephi or 4 Nephi by name): the books are the First and Second Book of Nephi, Jacob, Enos, Jarom, Omni, Words of Mormon, Mosiah, Alma, Helaman, two successive books each headed "The Book of Nephi" (the second "who is the son of Nephi, one of the disciples of Jesus Christ"), "Book of Mormon", Ether and Moroni. Many books open in the middle of a page.
* There is **no Preface**: the text opens with the title page (page 7), its verso with the 1829 copyright notice and a second title page, then 1 Nephi. The text is followed by the Testimony of the Three Witnesses and the Testimony of the Eight Witnesses.

## Source
Transcribed from a 587-page PDF scan of a copy held by the Historian's Office Library of The Church of Jesus Christ of Latter-day Saints, as published by the [Joseph Smith Papers](https://www.josephsmithpapers.org/paper-summary/book-of-mormon-1840/). The page images were downloaded with the [Archive Viewer](https://archiveviewer.org) tool and printed as a PDF (the PDF is not included in this repository). Each page is a photograph of the open book. The PDF has no text layer. The copy carries handwritten notes, ink and pencil marks, library labels and a large HISTORIAN'S OFFICE stamp; these are described in comments in the page files and not transcribed as text. Page 7 is the title page, page 8 its verso (copyright notice), page 9 a second title page, page 11 the opening of 1 Nephi (printed page 7), pages 576–577 the testimonies, and pages 578–587 blank leaves and the back cover and spine.

## What is Markdown?
Markdown is a simple way of writing formatted text using plain characters, such as `#` for headings and `*asterisks*` for *italics*. A Markdown file is still readable as ordinary text, and can also be displayed with formatting.
* Learn more at [markdown.org](https://markdown.org/).
* Tools for displaying, editing, or converting Markdown files: [https://markdown.org/tools/](https://markdown.org/tools/)

## Artificial Intelligence
Extracted with Claude Code from Anthropic using the Sonnet 5.5 model. Each page is transcribed from two crops of its scan image (there is no text layer or OCR), four pages at a time, by separate AI agents; a script then checks the structure of every page file, and doubtful marks were rechecked at higher zoom. A separate AI agent working blind then proofread all 569 text pages against the scan (the first 130 chosen by a local OCR comparison and a random sample, the rest afterwards). It corrected 9 small errors and logged 20 disagreements. The owner then decided those 20 and 41 doubtful readings marked in the pages against the scan, which changed about 15 readings; 32 doubtful readings remain marked in the page files. Where a mark was too worn to tell a comma from a period, the gap after it and whether the next word starts with a capital letter were used to decide. The text is meant to show what the page shows, so printer's spellings and errors, punctuation, hyphenation and paragraphing are kept. A few things are deliberately **not** reproduced: the thin space the type may put before `;`, `:`, `?` and `!`, handwriting, stamps, and ink specks, stains and bleed-through that are not letters or punctuation.

**This is an AI transcription. Only its doubtful places have been checked by a person; the book as a whole has not been proofread by a person.** The most likely places for a remaining error are punctuation on worn type, worn letters, and the squeezed left edge of pages near the spine. For anything that matters, check the scan.

**Status: all 587 pages of the scan are transcribed and structure-checked, and all 569 text pages were then proofread blind by a separate AI agent. The owner has decided the doubtful marks it left open against the scan; a full human proofread has not been done yet.** Expect remaining errors, especially colon versus semicolon and comma versus period, which are hard to tell apart in this scan, and worn letters that both AI readers may have normalized.

These files record how it was checked:

* [proofread-disagreements.md](proofread-disagreements.md): the edits, tie-breakers and disagreements from the blind proofread of all 569 text pages, and how the owner resolved them.
* [uncertain-log.md](uncertain-log.md): every doubtful reading and layout note recorded in the transcription, by page.
* [transcription-notes.md](transcription-notes.md): the layout of the scan, the conventions used and the review status.

## Rebuilding the combined files
```
python3 tools/compile_markdown.py   # book-of-mormon-1840.md
python3 tools/make_plaintext.py     # book-of-mormon-1840.txt
python3 tools/make_sparse.py        # book-of-mormon-1840-sparse.txt
python3 tools/make_typo_catalog.py  # printer-typos.md
python3 tools/make_uncertain_log.py # uncertain-log.md
python3 tools/check_structure.py    # mechanical checks of the page files
python3 tools/ocr_diff.py           # OCR-vs-transcription comparison (work/ocr/, needs tesseract)
```
See [tools/README.md](tools/README.md) for the full pipeline.
