# Verification Protocol (caller side)

This file defines the LOOP. It does not define the checks.
The checks live in one place only: the `verifier` agent.
Never restate check content here, and never self-assess against it.

## The loop

1. Draft the output.
2. Delegate to the `verifier` agent with all four inputs:
   - the draft
   - the original assignment prompt, complete, including every sub-question
   - the grading rubric
   - the output type: `essay`, `post`, or `reply`
   The output type is mandatory. The verifier enforces a different word
   count for each, and cannot select the right one without it.
3. Read the reply. It ends in `RESULT: PASS` or `RESULT: FAIL`.
4. On FAIL: fix EVERY listed issue, then return to step 2. A partial fix
   wastes an iteration, since the verifier re-reports what remains.
5. On PASS: proceed to the humanizer pass.
6. Cap: 5 attempts per version.

## Attempt log

Before proceeding past any attempt, record one line:

    v{N} attempt {i}: RESULT: <PASS|FAIL>

Keep the log for every version. A missing line means the verifier was not
called for that attempt, which is a skipped gate.

## Hard rules

- Do NOT show the user any draft until its log line reads `RESULT: PASS`,
  or the cap has been reached and the warning header is attached.
- Do NOT skip verification to save time or tokens.
- Self-assessment is not verification. "I checked it and it looks correct"
  does not satisfy this protocol. Only a Task call to the `verifier` agent
  returning `RESULT: PASS` satisfies it. The separation is the point:
  the verifier is adversarial and does not share the drafter's assumptions.

## At the cap

After 5 failed attempts, output the draft, but lead with this header:

    ## VERIFICATION FAILED after 5 attempts - NOT SUBMISSION READY
    Unresolved issues:
    - <issue, verbatim from the verifier>
    - <issue, verbatim from the verifier>

Then the draft. Do not silently present capped output as finished work, and
do not discard it. The user fixes the listed items by hand.

## Final scan, every output

After the humanizer pass, scan the final text for:

- U+2014 em dash and U+2013 en dash. Both are banned outright by the voice
  profile, which overrides any humanizer voice-sample behavior that would
  preserve them. Any occurrence must be rewritten before output.
- Citation integrity. The humanizer runs after verification, so its edits
  are not re-verified. Confirm every author name, year, page number, and
  DOI still matches what the verifier approved. The humanizer must not add
  or drop a citation, and must not invent one.
