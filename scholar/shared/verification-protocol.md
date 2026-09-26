# Verification Protocol (caller side)

This file defines the LOOP. It does not define the checks.
The checks live in one place only: the `scholar:verifier` agent.
Never restate check content here, and never self-assess against it.

## The pipeline

Every version of every output goes through these stages, in this order:

    draft -> GATE 1 (verifier) -> humanizer -> scan -> GATE 2 (verifier) -> output

Both gates call the same verifier with the same inputs, so both run every
check. Gate 1 proves the content earns full marks. Gate 2 proves the
humanizer did not cost any of them.

## Calling the verifier

Delegate to the `scholar:verifier` agent with:

- **Draft:** the text being checked
- **Prompt:** the complete assignment question and every professor
  instruction, word for word. For a reply: the student's post, plus any
  reply instructions.
- **Rubric:** the complete rubric for an essay or post. For a reply, the
  words "no rubric".
- **Source materials:** everything the user provided in the chat that the
  draft cites: readings, transcripts, documents, links, with author, year,
  title, and the passages used. Pass enough for the verifier to confirm
  each citation.
- **Output type:** `essay`, `post`, or `reply`
- **Title page details:** essays only, for this variant
- **Other versions:** the current text of every version or reply already
  finished for this request, if any

Pass the identical inputs at both gates. The reply ends in `RESULT: PASS` or
`RESULT: FAIL`.

## Gate 1: before the humanizer

1. Send the draft to the verifier.
2. On FAIL: fix EVERY listed issue, then send it again. A partial fix wastes
   an attempt, since the verifier re-reports what remains.
3. On PASS: keep a copy of this exact text. It is the verified fallback.
   Then go to the humanizer.
4. Cap: 5 attempts.

## Humanizer and scan

Run the `humanizer:humanizer` skill in embedded mode on the text that passed
Gate 1, with these constraints:

- No em dashes and no en dashes. Do not keep any.
- Do not add, remove, or change any citation, author, year, page number,
  or DOI.
- Keep every point that answers the prompt and every point that meets a
  rubric criterion. Change how things are said, not what is said.
- For a reply, keep the student's full name as the first line.

Then fix these before Gate 2, since they are cheap to catch here:

- Zero U+2014 em dash and zero U+2013 en dash.
- Every citation identical to the Gate 1 text.
- Length still inside the required range. The humanizer can shorten text,
  so re-count.

If the humanizer skill is unavailable, tell the user the humanizer pass was
skipped and still run Gate 2.

## Gate 2: after the humanizer

1. Send the humanized text to the verifier.
2. On FAIL: make the smallest edits that fix every listed issue, keeping
   the humanized wording everywhere else. Do NOT run the humanizer again,
   since that would reopen everything Gate 2 just checked. Send it again.
3. On PASS: this is the output.
4. Cap: 3 attempts.

## Attempt log

Before proceeding past any attempt, record one line:

    v{N} gate1 attempt {i}: RESULT: <PASS|FAIL>
    v{N} gate2 attempt {i}: RESULT: <PASS|FAIL>

A missing line means the verifier was not called for that attempt, which is
a skipped gate. Every version shown to the user must have a gate2 line
reading PASS, or be covered by a cap rule below.

## Hard rules

- Do NOT show the user any text until its Gate 2 log line reads
  `RESULT: PASS`, or a cap rule below applies.
- Do NOT skip either gate to save time or tokens.
- Self-assessment is not verification. Only an Agent (Task) call to the
  `scholar:verifier` agent returning `RESULT: PASS` satisfies a gate. The
  separation is the point: the verifier is adversarial and does not share
  the drafter's assumptions.
- The dash ban covers everything printed, including labels and notes. Use
  a colon or a period instead.

## At a cap

**Gate 1 cap** (5 failures): the content does not meet the prompt and
rubric. Skip the humanizer and Gate 2. Output the draft, led by:

    ## VERIFICATION FAILED after 5 attempts - NOT SUBMISSION READY
    Unresolved issues:
    - <issue, verbatim from the verifier>

**Gate 2 cap** (3 failures): output the Gate 1 fallback instead of the
humanized text. It passed every check. Say in one line that this version is
shown without the humanizer pass. Never output humanized text that failed
Gate 2.
