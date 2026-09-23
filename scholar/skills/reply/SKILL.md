---
name: reply
description: >
  Write peer replies for discussion posts. 100 to 130 words each, engaging the
  classmate's specific argument with a source and a closing question. Multiple
  distinct reply sets. Never shows a reply that has not passed the verifier.
allowed-tools: Agent, Task, Skill, Bash, Write, Read, Glob, Grep
---

# Write peer replies

**Do not show the user any reply until the verifier agent has returned
`RESULT: PASS` for it twice: once before the humanizer (Gate 1, step 6)
and once after it (Gate 2, step 8).** No previews, no "here is a first
pass while I check." The only exceptions are the cap rules in
`shared/verification-protocol.md`, which either attach a warning header or
fall back to the Gate 1 text.

## 1. Read the reference files

- `${CLAUDE_PLUGIN_ROOT}/shared/voice-profile.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/apa7-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/verification-protocol.md`

If a path does not resolve, Glob for `**/shared/voice-profile.md`.

## 2. Identify the course

Data root is `${CLAUDE_PROJECT_DIR}/scholar-data/`. If it does not exist,
create it with `courses.md` from `${CLAUDE_PLUGIN_ROOT}/templates/courses.md`.
One active course: use it. Several: ask. None: run `setup-course` inline.

## 3. Load context

Read `{course}/feedback.md`. Every entry is a hard constraint.

Read `{course}/knowledge.md` for sources you can cite. Replies need a real
source, and the unit readings are where it comes from.

## 4. Get the classmate posts

The user pastes one or more classmate posts. If they have not, ask for them.

Ask how many distinct reply sets they want, if they did not say. A set contains
one reply per classmate post.

## 5. Draft each reply

Per reply, 100 to 130 words. Count it.

Every reply must:

- Engage that classmate's **specific** argument. Name the actual claim they
  made. Generic praise that would fit any post is a failure of this step.
- Reference at least one real source, from the unit readings or clearly
  relevant prior knowledge, cited in APA 7.
- End with a genuine question that advances the discussion. Not rhetorical,
  and not something their post already answered.

Across sets, do not repeat the same opening, the same source, or the same
question. Each set takes a different angle on the classmate's points.

Voice profile applies. No em dashes, no en dashes. No sycophantic opener
("Great post!"). Do not invent a source, a statistic, or a quotation from the
classmate's post.

## 6. Gate 1: verify each reply. Hard gate.

Follow `shared/verification-protocol.md` exactly. For each reply, delegate
to the `scholar:verifier` agent with the reply, the classmate's post as the prompt context, the
rubric if the user supplied one, and output type
`reply`. On FAIL, fix every listed issue and resubmit. Log each attempt:

    v{N} gate1 attempt {i}: RESULT: <PASS|FAIL>

If the user supplied no rubric, pass the words "no rubric supplied" as the
rubric input, at both gates. The verifier then skips CHECK 2 and runs
checks 1, 3, and 4.

Self-assessment is not verification. Only an Agent (Task) call to the
`scholar:verifier` agent returning `RESULT: PASS` satisfies this step.

On PASS, keep an exact copy of the text. It is the verified fallback if
Gate 2 cannot pass. Cap at 5 attempts; at the cap, follow the protocol's
Gate 1 cap rule and skip steps 7 and 8.

## 7. Humanizer pass. Invisible.

Only after Gate 1 passes. Invoke the `humanizer:humanizer` skill in
**embedded mode**, which returns only the final text. Pass these
constraints with the text:

- Em dashes and en dashes are banned outright. The voice profile is the
  governing writing sample and it forbids them. Do not preserve them.
- Do not add or remove any citation, author name, year, page number, or DOI.
- Keep every point that answers the prompt and every point that meets a
  rubric criterion. Change how things are said, not what is said.

Then run the protocol's scan: zero U+2014, zero U+2013, every citation
identical to the Gate 1 text, and word count still inside 100 to 130. The window is
narrow, so re-count and fix any drift.

If the `humanizer:humanizer` skill is unavailable, apply the voice profile's
"What to avoid" list yourself, tell the user the humanizer pass was
skipped, and still run step 8.

## 8. Gate 2: verify again after the humanizer. Hard gate.

The humanizer rewrote the text, so Gate 1's PASS no longer covers it. Send
the humanized text to the `scholar:verifier` agent with the same inputs as
step 6. Log each attempt:

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

## 9. Output

Print the replies as formatted text in the chat, grouped by set and labeled
with which classmate post each answers. State each word count.
