# Proofread results: edits, tie-breakers and disagreements

Generated from the blind proofread logs (`work/proof-log-*.md`, local). A second AI agent re-read each page against the scan without seeing the transcriber's notes. It edited the page file only when certain; where it read a mark differently from the file but could not be certain, it logged a **disagreement** and left the file as it was. The disagreements below are for the owner to decide against the scan (PDF page numbers; printed page = PDF page - 4).

**All 569 text pages (PDF pages 7, 9 and 11-577) were proofread this way**: first the 70 pages flagged by the OCR comparison and a random sample of 60, then, because the owner asked for full coverage, the other 439. Pages 1-6, 8, 10 and 578-587 (covers, labels, the title-page verso, blank leaves) have no text of their own and were not proofread. Result: 9 edits plus 2 tie-breaker uses (one of which changed a mark), and 20 disagreements.

## Edits made (9)

- **63**: title: was "# THE SECOND BOOK OF NEPHI" -> now "# THE SECOND BOOK OF NEPHI." (zoom 3 shows a plain period after NEPHI)
- **126**: para 4 line 1: was "the people of Nephi, under" -> now "the poople of Nephi, under" (scan plainly prints p-o-o-p-l-e at zoom 3; printer error restored)
- **182**: "what teach ye this people?—" -> "people!—" (zoom 3 shows a plain exclamation mark before the dash)
- **215**: heading: was "## CHAPTER XIII" -> now "## CHAPTER XIII." (scan prints a full stop after XIII)
- **243**: line "how have ye forgotten the tradition": was "the" -> now "tho" (scan prints t-h-o before tradi-tion)
- **295**: first line: was "For behold" -> now "<!-- cont --> For behold" (cont marker; first line flush-left with the lines below, not indented)
- **325**: line 5: was "thoughts be directed" -> now "thoughts he directed" (zoom 3 shows h-e, printer error, file had normalized to be)
- **406**: line "father, insomuch": was "father," -> now "father." (zoom 3 shows a plain round dot, no tail, before lowercase insomuch)
- **468**: line 1: was "in which I have suffered" -> now "in the which I have suffered" (scan prints "in the which"; dropped word)

## Tie-breaker uses (2)

- **386**: p.382 line 1 "weary, because": kept comma (tight gap, lowercase next word)
- **531**: "And behold, O Lord. in them": "," -> "." (zoom 3 shows a plain round dot at baseline, no tail; gap tight before lowercase "in" so signals disagreed, shape decides; uncertain comment removed)

## Disagreements for the owner (20)

Each line: the page, then what the proofreader reported (what the file has, what the scan seems to show, and why it was left).
 
- **69**: para 1 "had no children": file has "no children", I read "nochildren" (no visible word space on scan; could be tight justification, not certain)
- **97**: last paragraph, "such as was in": file has "as", I read "us" at native size (a/u unclear, possibly worn a; not zoomed)
- **134**: "servant, come, let us go down": file has comma after "come", I read a possible period (dot on baseline, but tight gap and lowercase next word, so tie-breaker gives comma; kept)
- **182**: line-end "riches?", "law of Moses?", "What say ye?": file has "?", at the clipped right edge the marks look like "!" (hook cut off by scan edge, not certain)
- **184**: "keep it holy." : file has ".", I read ":" (faint upper dot at 3x, borderline)
- **209**: "in my name are they called": file has "are" (with uncertain comment), I read "ure" at native size (worn/ambiguous letter; not edited)
- **218**: "all the wars": file has "wars", scan letter 3 looks like t/f-shaped (could be a broken r, "wats"); borderline worn type, not edited
- **218**: header: file has "214 | BOOK OF MOSIAH."; scan crop cuts the head off (only "214" partly visible; the legible "BOOK OF MOSIAH." is mirrored bleed-through), so the running head text cannot be confirmed; not edited
- **220**: first word of chapter text: file has "NOW", I read "Now" (capital N followed by lowercase-form letters, slightly heavier type)
- **235**: "unquenchable" (line "even an unquenchable fire"): file has "unquenchable", first n looks like u at native size (worn n; zoom unavailable), left as file
- **274**: last paragraph "began to pour": file has no mark, I see a small faint comma-like mark below baseline after "began" at zoom 3 (could be a speck; tight gap)
- **293**: line 5 "brethren has he loosed": file has "brethren", scan shows a worn r that reads like "brethıen" (kept; worn letter reads as expected letter)
- **360**: line 12 (narrow condensed type, "which conse-"): file has "conse-quences", I read "couse-" (narrow letter after o looks like u, not clearly n at zoom)
- **407**: first line "inton": file has "inton" with no edge note; the left edge of the scan is squeezed at the spine and the word may be cut ("...inton"), so a left-edge comment might be wanted (not edited, borderline)
- **432**: "God; yea, behold": file has "yea, behold", I read "yea,behold" (word space after comma looks absent, likely tight justification)
- **457**: para 2 "their exceeding great riches": file has "exceeding", I read "exeeeding" (third letter looks like a closed e at 3x, but c/e worn-type ambiguity, not edited)
- **472**: "hate.thine" and "have-their": file has these marks; scan shows a tiny dot and short dash that may be specks (word gaps look normal); left as file
- **522**: line "come unto the knowledge of the people; and it shall be": file has ";", mark looks like ":" at native size (borderline, not zoomed)
- **538**: para 3 "and, multiply": file has comma after "and"; the mark sits on a hand-drawn pencil line, so it may be a pen stroke rather than type (not certain, not edited)
- **548**: "had-spoken": file has hyphen, scan shows a raised dot/short mark between "had" and "spoken" (could be hyphen or speck); not edited

## Resolved by the owner (2026-10-23)

The owner decided all 20 disagreements against the scan with `tools/make_review_checklist.py` (`work/review/checklist.html`, local), together with the 41 `uncertain` comments in the page files. "Keep" means the page file was left as it was; its comment, if any, stays.

**Changed in the page files**
- **69**: "no children" -> "nochildren" (no word space printed)
- **218**: the running head was confirmed on the full photo: "214 | BOOK OF MOSIAH." (the band crop had cut it off; the proofreader's doubt came from that crop, and the file was already right)
- **220**: "NOW" -> "Now"
- **407**: first word "inton" -> "ianton" (continues "Gad-" on 406; left edge squeezed at the spine); comment added
- **457**: "exceeding" -> "exeeeding"
- **472**: "hate.thine" -> "hate thine", "have-their" -> "have their"
- **538**: "and, multiply" -> "and multiply"
- **548**: "had-spoken" -> "had spoken"

**Kept as in the file**: 97, 134, 182, 184, 209, 218 ("wars"), 235, 274, 293, 360, 432, 522.

**Uncertain comments resolved (page files and `uncertain-log.md`)**
- changed, comment removed: 91 (mark after "neighbor" is ":"), 105 ("CHAPTER XI."), 107 ("this"), 179 ("possessed"), 184 ("things?"), 365 ("land"), 379 ("And"), 386 (comma kept), 527 ("chirdren")
- 198: the hyphen in "de-" kept, comment kept
- the other 30: kept, comments left in place

**Page 361**: the running head prints "257" (expected "357"); a layout comment records the printer's misnumbering. `check_structure.py` keeps warning about it, as intended.
