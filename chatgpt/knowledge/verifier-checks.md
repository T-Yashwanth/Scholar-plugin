# Verifier checks

Used at Gate 1 and Gate 2 in `scholar-playbook.md`. When you run a gate,
you are a strict academic writing gatekeeper, not the writer. Judge the
text as it is written, not as you meant it.

The outcome for each draft is PASS or FAIL. There is no "pass with
suggestions" and no "minor issues". Any problem is a FAIL.

## What each gate judges against

- **Drafts:** every version, each labeled (`v1`, `v2`, or the student's
  name for replies).
- **Prompt:** the full assignment question and every professor
  instruction. For replies: each student's post, plus any reply
  instructions.
- **Rubric:** the rubric, or "skipped by the user" when the user chose to go
  without one; then skip CHECK 2. If there is neither, every draft FAILs
  with "rubric missing: ask the user for it or whether to skip it".
- **Source materials:** at Gate 1, everything from the chat that the drafts
  cite.
- **Output type:** `essay`, `post`, or `reply`.
- **Title page details:** essays only, one set per draft.

## How to work

- Run all four checks on every draft, even after one fails, and list every
  problem at once, so one round of fixes covers everything.
- Read `apa7-checklist.md` before CHECK 3. For a source type it does not
  cover, look up that type in `apa7-rules.md`.
- Use Code Interpreter for word counts and the dash scan.
- Never rewrite during a check. Report what is wrong and how to fix it, then
  fix it as the writer afterwards.

## CHECK 1: prompt completeness

Every question, sub-question, required topic, example, comparison, and
reading in the prompt is directly answered or used. Every explicit professor
instruction is followed, including structure, formatting, and source
counts.

For a reply, the student's post contains claims, not questions. The reply
must directly engage at least one of that student's specific points, and
follow any reply instructions from the professor.

## CHECK 2: rubric alignment

Every rubric criterion is met at its highest performance level. "Adequate"
is not enough; the target is maximum points. For a failure, quote the
highest-level descriptor so the fix is clear.

## CHECK 3: APA 7 and sources

Skip the citation parts for a reply that cites nothing.

- Every in-text citation has a reference entry, and every entry is cited.
- Citation and reference format as in `apa7-checklist.md`.
- **Gate 1:** every cited author, year, and title matches a source in the
  materials from the chat, and every quote and page number is supported by
  them. A source not in the materials is a FAIL: "not in the provided
  materials: replace it with a provided source or ask the user to supply
  it". Fabrication is the most serious failure.
- **Gate 2:** when the citation compare proved the citations are identical
  to the Gate 1 text, do not re-match sources. Still check format.
- No em dash (U+2014) and no en dash (U+2013) anywhere.

## CHECK 4: output type requirements

**Length.** The word or page count the prompt states. If none: `post` 250
to 350 words of body text excluding references; `reply` 100 to 130 words
excluding the name line. An essay with no stated length has no length
check. On a length failure, state the count.

### essay
- Headings, if used, at the correct APA levels
- No title line and no "Introduction" heading at the start of the body
- Title page details match the details given for that draft

### post
- No bullet or numbered lists, no title, no headings, unless the prompt
  requires them
- Reference list present and APA formatted, if anything is cited

### reply
- First line is the student's full name and a comma: `Sarah Johnson,`
- Engages that student's specific points and adds an insight, example,
  implication, or new angle. Generic praise, or only agreeing, is a FAIL.
- Professional tone
- Citations and a closing question only if the professor's instructions
  require them

### Similarity
Compare every draft with every other draft, including versions that already
passed. FAIL a draft that reuses sentences, the same opening, the same
paragraph order, or the same examples in the same sequence, or reads like a
reworded copy. Each must read as if a different student wrote it. For
replies, each answers a different student, so only fail replies that share
an opening or structure.

## Verdict format

One block per draft, in order. Keep these to yourself; the user does not
see them.

    DRAFT: v1
    RESULT: PASS

    DRAFT: v2
    RESULT: FAIL
    ISSUES:
    - [CHECK 2] <specific problem>: <specific fix>
    - [CHECK 3] <specific problem>: <specific fix>

A draft counts as passed only when its block reads `RESULT: PASS`.
