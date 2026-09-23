# Verification Protocol (caller side)

This file defines the LOOP. It does not define the checks.
The checks live in one place only: the `scholar:verifier` agent.
Never restate check content here, and never self-assess against it.

## The pipeline

Every version of every output goes through these stages, in this order:

    draft -> GATE 1 (verifier) -> humanizer -> scan -> GATE 2 (verifier) -> output

Both gates call the same verifier with the same inputs, so both run every
check: prompt completeness, rubric at the highest level, APA 7, and the
output type rules. Gate 1 proves the content earns full marks. Gate 2
proves the humanizer did not cost any of them.

## Calling the verifier

Delegate to the `scholar:verifier` agent with all four inputs:

- the draft
- the original assignment prompt, complete, including every sub-question
- the grading rubric
- the output type: `essay`, `post`, or `reply`

The output type is mandatory. The verifier enforces a different word count
for each, and cannot select the right one without it. Pass the identical
prompt and rubric at both gates.

The reply ends in `RESULT: PASS` or `RESULT: FAIL`.

## Gate 1: before the humanizer

1. Send the draft to the verifier.
2. On FAIL: fix EVERY listed issue, then send it again. A partial fix wastes
   an attempt, since the verifier re-reports what remains.
3. On PASS: keep a copy of this exact text. It is the verified fallback.
   Then go to the humanizer.
4. Cap: 5 attempts.

## Humanizer and scan

Run the humanizer on the text that passed Gate 1, with the constraints the
calling skill passes. Then fix these mechanically before Gate 2, since they
are cheap to catch here and would otherwise cost a Gate 2 attempt:

- Zero U+2014 em dash and zero U+2013 en dash. The voice profile bans both
  and overrides any humanizer voice-sample behavior that would keep them.
- Every author name, year, page number, and DOI identical to the Gate 1
  text. No citation added, dropped, or invented.
- Word count still inside the output type's range. The humanizer can
  shorten text, so re-count.

## Gate 2: after the humanizer

1. Send the humanized text to the verifier.
2. On FAIL: make the smallest edits that fix every listed issue, keeping
   the humanized wording everywhere else. Do NOT run the humanizer again,
   since that would reopen everything Gate 2 just checked. Send it again.
3. On PASS: this is the output.
4. Cap: 3 attempts. The text already passed once, so the fixes should be
   small. If they are not converging, the humanizer did real damage.

## Attempt log

Before proceeding past any attempt, record one line:

    v{N} gate1 attempt {i}: RESULT: <PASS|FAIL>
    v{N} gate2 attempt {i}: RESULT: <PASS|FAIL>

Keep the log for every version. A missing line means the verifier was not
called for that attempt, which is a skipped gate. Every version shown to
the user must have a gate2 line reading PASS, or be covered by a cap rule
below.

## Hard rules

- Do NOT show the user any text until its Gate 2 log line reads
  `RESULT: PASS`, or a cap rule below applies.
- Do NOT skip either gate to save time or tokens.
- Self-assessment is not verification. "I checked it and it looks correct"
  does not satisfy this protocol. Only an Agent (Task) call to the
  `scholar:verifier` agent returning `RESULT: PASS` satisfies it. The
  separation is the point: the verifier is adversarial and does not share
  the drafter's assumptions.

## At a cap

**Gate 1 cap** (5 failures): the content itself does not meet the prompt
and rubric. Skip the humanizer and Gate 2. Output the draft, led by:

    ## VERIFICATION FAILED after 5 attempts - NOT SUBMISSION READY
    Unresolved issues:
    - <issue, verbatim from the verifier>
    - <issue, verbatim from the verifier>

**Gate 2 cap** (3 failures): output the verified fallback from Gate 1
instead of the humanized text. That text passed every check. Say, in one
line, that this version is shown without the humanizer pass because the
rewrite could not keep full marks. Never output humanized text that
failed Gate 2.

Do not silently present capped output as finished work, and do not discard
it. The user fixes any listed items by hand.
