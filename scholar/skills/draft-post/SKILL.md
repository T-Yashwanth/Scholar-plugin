---
name: draft-post
description: >
  Draft a discussion post in APA 7 format. 250 to 350 words, essay format,
  no title page. Multiple distinct versions. Never shows a draft that has not
  passed the verifier agent. Use for any discussion board assignment.
allowed-tools: Agent, Task, Skill, Bash, Write, Read, Edit, Glob, Grep
---

# Draft a discussion post

**Do not show the user any draft until the verifier agent has returned
`RESULT: PASS` for it twice: once before the humanizer (Gate 1, step 7)
and once after it (Gate 2, step 9).** No previews, no "here is a first
pass while I check." The only exceptions are the cap rules in
`shared/verification-protocol.md`, which either attach a warning header or
fall back to the Gate 1 text.

## 1. Read the reference files

- `${CLAUDE_PLUGIN_ROOT}/shared/voice-profile.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/apa7-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/verification-protocol.md`

If a path does not resolve, Glob for `**/shared/voice-profile.md`. Do not
proceed without the voice profile.

## 2. Identify the course

Data root is `${CLAUDE_PROJECT_DIR}/scholar-data/`. If it does not exist,
create it with `courses.md` from `${CLAUDE_PLUGIN_ROOT}/templates/courses.md`.

Read `courses.md`. One active course: use it. Several: ask which. None: run the
`setup-course` interview inline, then continue.

## 3. Load course context

Read `{course}/knowledge.md` and `{course}/feedback.md`. Every feedback entry
is a hard constraint. Cross-course material only where it genuinely fits.

## 4. Auto-save new knowledge

If the pasted readings contain material not in `knowledge.md`, append it under
a `## Unit N: {topic}` header before drafting.

## 5. Ask the version count

"How many distinct versions?" if the user did not say.

## 6. Analyze and draft

Internal analysis first, not shown: every question and sub-question, every
rubric criterion and its top performance level, and every stated requirement.
Ask for the rubric if it was not supplied.

Then draft each version:

- 250 to 350 words of body text, excluding the reference list. Count it.
- Essay format. No title. No headings. No bullet or numbered lists, unless the
  prompt explicitly requires them.
- Assign each version a different analogy domain from the voice profile before
  writing, and give each a different angle and structure. Different versions
  must not share a hook or an argument shape.
- APA 7 in-text citations, with a reference list at the end.
- Voice profile throughout. No em dashes, no en dashes.
- No "In today's world" opener. No "In conclusion" closer. End on a hard
  declarative line.

## 7. Gate 1: verify each version. Hard gate.

Follow `shared/verification-protocol.md` exactly. For each version, delegate
to the `scholar:verifier` agent with the draft, the complete prompt, the rubric, and output type
`post`. On FAIL, fix every listed issue and resubmit. Log each attempt:

    v{N} gate1 attempt {i}: RESULT: <PASS|FAIL>

Self-assessment is not verification. Only an Agent (Task) call to the
`scholar:verifier` agent returning `RESULT: PASS` satisfies this step.

On PASS, keep an exact copy of the text. It is the verified fallback if
Gate 2 cannot pass. Cap at 5 attempts; at the cap, follow the protocol's
Gate 1 cap rule and skip steps 8 and 9.

## 8. Humanizer pass. Invisible.

Only after Gate 1 passes. Invoke the `humanizer:humanizer` skill in
**embedded mode**, which returns only the final text. Pass these
constraints with the text:

- Em dashes and en dashes are banned outright. The voice profile is the
  governing writing sample and it forbids them. Do not preserve them.
- Do not add or remove any citation, author name, year, page number, or DOI.
- Keep every point that answers the prompt and every point that meets a
  rubric criterion. Change how things are said, not what is said.

Then run the protocol's scan: zero U+2014, zero U+2013, every citation
identical to the Gate 1 text, and body word count still inside 250 to 350. The
humanizer can shorten text, so re-count and fix any drift.

If the `humanizer:humanizer` skill is unavailable, apply the voice profile's
"What to avoid" list yourself, tell the user the humanizer pass was
skipped, and still run step 9.

## 9. Gate 2: verify again after the humanizer. Hard gate.

The humanizer rewrote the text, so Gate 1's PASS no longer covers it. Send
the humanized text to the `scholar:verifier` agent with the same inputs as
step 7. Log each attempt:

    v{N} gate2 attempt {i}: RESULT: <PASS|FAIL>

On FAIL, make the smallest edits that fix every listed issue and keep the
humanized wording everywhere else. Do not run the humanizer again. Cap at 3
attempts; at the cap, follow the protocol's Gate 2 cap rule and output the
Gate 1 fallback instead.

Do not show a before and after. Do not mention the humanizer, except when
a cap rule or an unavailable humanizer requires it.

The dash ban covers everything you print, not only the body text. Labels,
headers, word counts, and any commentary around the output must also be
free of em and en dashes. Use a colon or a period instead.

## 10. Output

Print each version as formatted text in the chat, ready to paste into the LMS.
No .docx. Label each version and state its body word count.
