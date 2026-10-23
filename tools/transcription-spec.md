# Transcription spec — 1840 Robinson & Smith (Nauvoo) Book of Mormon

Instructions for transcribing agents. Source: `1840-Book-of-Momron.pdf` (587 pages, photos of a book, no text layer). Files are keyed to the **PDF page number** (3 digits). Printed folio = PDF page − 4 in the main text (PDF 11 = p. 7, where 1 Nephi opens; 21 = p. 17).

Inputs for PDF page N (NNNN = 4-digit) in `work/`: `img/pNNNN_1_top.jpg` and `img/pNNNN_2_bottom.jpg`, two bands of the text block at native resolution that overlap slightly (do not duplicate lines in the overlap). View **both** bands of every page with Read before writing it. If an image fails, stop and report the page as failed; never transcribe unseen.
For a doubtful spot only: `~/.venvs/lds-transcribe/bin/python tools/prepare_images.py --pages N --zoom 2 --out work/zoom` (then delete it).
Output: `book-of-mormon-1840-pages/page-NNN.md`. Skip pages whose file exists. Write each file right after viewing its page.

## Rules
- **Write what is printed, never what you think it should say.** Printer's errors, odd spellings, names, grammar, doubled or missing words, damaged type and wrong running heads are kept. Do not correct from the 1830 or 1837 editions, the KJV, the manuscripts or memory. This 1840 text is a revision of 1837; it differs from it in places, so reading from memory is the main risk. Read letter by letter.
- Doubtful reading: best guess plus `<!-- uncertain: … -->` right after it. Unreadable: `[illegible]`.
- Line-end hyphenation is joined into the whole word; words hyphenated in the original stay hyphenated (grep other page files if ambiguous).
- No verse numbers, no marginal notes, one wide column, ordinary punctuation. Record punctuation, capitals after colons, `&c.` etc. exactly. Write NO space before `; : ? !` (the type has a thin space; not transcribed).
- Comma vs period when the mark is uncertain: more space and a capitalized next word = period; less space and a lowercase next word = comma. Colon vs semicolon: judge the dots/tail at zoom 2 when in doubt.
- Italic = `*italic*` (no space inside the asterisks). Small caps = capitals; ordinary capitalized words keep their case (`And now`).
- Ink specks, bleed-through (mirror-image text from the reverse leaf, strongest at the left/bottom), dirt lines, photo borders, the book spine and page-edge shading are not text. Ignore without a comment. Use `uncertain` only for a real mark in doubt.

## Format
```
<!-- image NNN -->  (NNN = PDF page number)
**Header:** 8 | FIRST BOOK OF NEPHI.   <- running head, parts separated by " | ", as printed (omit if none)

# THE FIRST BOOK OF NEPHI:               <- book title; any printed subtitle as plain/italic text
## CHAPTER II.                           <- chapter heading, numerals as printed
<!-- decorative ornament printed above the chapter heading -->   (on its own line above `## CHAPTER`, only where an ornament is printed)

AND it came to pass ...                  <- one paragraph per printed paragraph

---

Footer: 2*                               <- signature mark / catchword not in the Header (omit if none)
```
- Even pages have the folio on the left of the head, odd on the right. Pages that open a book have no running head.
- A printed paragraph starts with an indented first line. If the page's first line is flush-left (continuing the previous page's paragraph) start it with `<!-- cont --> ` even if the previous page ended with a full stop. If the page ends mid-paragraph, write the fragment; a page-end hyphen stays (`vis-`) and the next page starts `<!-- cont --> ions …`.
- Chapter summaries (if printed under a heading) are italic paragraphs as printed. A new book opening mid-page: ornament comment, `# TITLE`, `## CHAPTER`, summary; the running head stays that of the book the page began in (note it in a comment).
- Text cut off by the edge of the scan: write the visible fragment, never complete it, and note which edge in a comment at the top.
- Front and back matter (title page, copyright verso, testimonies): transcribe in full as stacked lines in printed order and case, with a layout comment. Handwriting, stamps (e.g. HISTORIAN'S OFFICE), labels and bookplates: describe in an HTML comment only, not as text. A page with nothing to read: the page comment and a one-line description comment.
- No commentary, summaries or modern corrections.

## Agent run notes
- A batch is 4 pages. Run `python3 tools/prepare_images.py --pages A-B` first, `--clean` when done. Final reply: pages written, pages failed, anything unusual (brief).
