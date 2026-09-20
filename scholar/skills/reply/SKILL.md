---
name: reply
description: >
  Write peer replies for discussion posts. 100 to 130 words each, engaging the
  classmate's specific argument with a source and a closing question. Multiple
  distinct reply sets. Never shows a reply that has not passed the verifier.
allowed-tools: Bash, Write, Read, Glob, Grep
---

# Write peer replies

**Do not show the user any reply until the verifier agent has returned
`RESULT: PASS` for it.** The only exception is the 5-attempt cap in step 6,
which carries a warning header.

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

## 6. Verify each reply. Hard gate.

Follow `shared/verification-protocol.md`. Delegate each reply to the
`scholar:verifier` agent with the reply, the classmate's post as the prompt context, the rubric if
the user supplied one, and output type `reply`. Log each attempt:

    v{N} attempt {i}: RESULT: <PASS|FAIL>

Self-assessment is not verification. Only a Task call to the `scholar:verifier` agent
returning `RESULT: PASS` satisfies this step. Cap at 5 attempts per reply, then
attach the protocol's warning header.

If the user supplied no rubric, tell the verifier so, and have it run checks
1, 3, and 4 only.

## 7. Humanizer pass. Invisible.

Only after `RESULT: PASS`. Invoke the `humanizer` skill in **embedded mode**,
passing these constraints:

- Em and en dashes are banned by the governing voice profile.
- Do not add or remove any citation, author, year, page number, or DOI.

Then scan: zero U+2014, zero U+2013, citations unchanged, and word count still
inside 100 to 130. The window is narrow, so re-count after the rewrite and fix
any drift.

Do not mention the humanizer.

The dash ban covers everything you print, not only the body text. Labels,
headers, word counts, and any commentary around the output must also be free
of em and en dashes. Use a colon or a period instead.

## 8. Output

Print the replies as formatted text in the chat, grouped by set and labeled
with which classmate post each answers. State each word count.
