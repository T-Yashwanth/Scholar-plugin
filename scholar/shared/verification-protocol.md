# Verification Protocol (caller side)

This file defines the LOOP. It does not define the checks.
The checks live in one place only: the `scholar:verifier` agent.
Never restate check content here, and never self-assess against it.

## The pipeline

All versions of one request (every variant, or every reply) move through
the pipeline together:

    draft all -> GATE 1 -> humanize all -> citation compare -> GATE 2 -> output

Each gate is one verifier call covering every version, plus retry calls for
the versions that failed. Gate 1 proves the content earns full marks. Gate 2
proves the humanizer did not cost any of them.

## Calling the verifier

One call per round, with every version that still needs a verdict.
Delegate to the `scholar:verifier` agent with:

- **Gate:** `1` or `2`
- **Drafts:** each version to judge, labeled `v1`, `v2`, and so on, or with
  the student's name for replies
- **Reference versions:** versions that already passed this gate, labeled.
  Sent only on retry rounds, so the similarity check still covers them.
- **Prompt:** the complete assignment question and every professor
  instruction, word for word. For replies: each student's post, labeled to
  match its reply, plus any reply instructions.
- **Rubric:** the complete rubric, or the words "skipped by the user" when
  the user was asked and chose to go without one. Never send "skipped" on
  your own.
- **Source materials (Gate 1 only):** everything from the chat that the
  drafts cite: readings, transcripts, documents, links, with author, year,
  title, and the passages used
- **Citations confirmed (Gate 2 only):** the statement "every in-text
  citation and reference entry is identical to the Gate 1 text"
- **Output type:** `essay`, `post`, or `reply`
- **Title page details:** essays only, one set per draft
- **Checklist path:** the full path of `shared/apa7-checklist.md`

The reply has one `DRAFT:` block per judged version, each with a `RESULT:
PASS` or `RESULT: FAIL` line. On FAIL the block lists every issue at once.

## Gate 1: before the humanizer

1. Send all versions in one call.
2. For each FAIL: fix EVERY listed issue in that version.
3. Retry: send only the fixed versions as drafts, and the versions that
   already passed as reference versions. Repeat until every version passes
   or hits the cap.
4. When a version passes, keep an exact copy. It is that version's verified
   fallback.
5. Cap: 5 rounds per version.

## Humanize

Run the `humanizer:humanizer` skill in embedded mode **once, on all the
versions that passed Gate 1 together**, each clearly labeled so none is
merged or lost. Pass these constraints:

- Return every version separately, with its label. Keep them as different
  from each other as they are now.
- No em dashes and no en dashes. Do not keep any.
- Do not add, remove, or change any citation, author, year, page number,
  or DOI.
- Keep every point that answers the prompt and every point that meets a
  rubric criterion. Change how things are said, not what is said.
- For a reply, keep the student's full name as the first line.

If the humanizer skill is unavailable, tell the user the humanizer pass was
skipped and still run Gate 2.

## Citation compare and scan

Before Gate 2, for each version, do this yourself:

1. List every in-text citation and every reference entry in the Gate 1 text
   and in the humanized text. They must be identical: same authors, years,
   page numbers, DOIs, and the same number of each. Put back anything the
   humanizer changed, exactly as it was in the Gate 1 text.
2. Zero U+2014 em dash and zero U+2013 en dash.
3. Length still inside the required range. The humanizer can shorten text,
   so re-count.

Only when step 1 holds for every version may Gate 2 skip the source
materials. If a citation cannot be restored exactly, send that version to
Gate 2 with the source materials and without "citations confirmed".

## Gate 2: after the humanizer

1. Send all humanized versions in one call, with "citations confirmed" and
   without the source materials.
2. For each FAIL: make the smallest edits that fix every listed issue,
   keeping the humanized wording everywhere else. Do NOT run the humanizer
   again. If a fix touches a citation, it must match the Gate 1 text.
3. Retry: failed versions as drafts, passed ones as reference versions.
4. Cap: 3 rounds per version.

## Attempt log

After every verifier call, record one line per version judged in it:

    v{N} gate1 round {i}: RESULT: <PASS|FAIL>
    v{N} gate2 round {i}: RESULT: <PASS|FAIL>

A version with no line for a round was not checked in that round, which is
a skipped gate. Every version shown to the user must have a gate2 line
reading PASS, or be covered by a cap rule below.

## Hard rules

- Do NOT show the user any text until its Gate 2 line reads `RESULT: PASS`,
  or a cap rule below applies.
- Do NOT skip either gate to save time or tokens. Batching versions into one
  call is how this protocol saves them.
- Self-assessment is not verification. Only an Agent (Task) call to the
  `scholar:verifier` agent returning `RESULT: PASS` satisfies a gate. The
  citation compare above is a mechanical copy check, not a verdict.
- The dash ban covers everything printed, including labels and notes. Use a
  colon or a period instead.

## At a cap

**Gate 1 cap** (5 rounds failed): that version's content does not meet the
prompt and rubric. It skips the humanizer and Gate 2. Output it, led by:

    ## VERIFICATION FAILED after 5 attempts - NOT SUBMISSION READY
    Unresolved issues:
    - <issue, verbatim from the verifier>

**Gate 2 cap** (3 rounds failed): output that version's Gate 1 fallback
instead of the humanized text. It passed every check. Say in one line that
this version is shown without the humanizer pass. Never output humanized
text that failed Gate 2.
