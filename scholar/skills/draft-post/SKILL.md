---
name: draft-post
description: >
  Draft a discussion post in APA 7 format. 250 to 350 words, essay format,
  no title page. Multiple distinct versions. Never shows a draft that has not
  passed the verifier agent. Use for any discussion board assignment.
allowed-tools: Task, Skill, Bash, Write, Read, Edit, Glob, Grep
---

# Draft a discussion post

**Do not show the user any draft until the verifier agent has returned
`RESULT: PASS` for it.** No previews. The only exception is the 5-attempt cap
in step 7, which carries a warning header.

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

## 7. Verify each version. Hard gate.

Follow `shared/verification-protocol.md`. Delegate to the `verifier` agent with
the draft, the complete prompt, the rubric, and output type `post`. On FAIL,
fix every issue and resubmit. Log each attempt:

    v{N} attempt {i}: RESULT: <PASS|FAIL>

Self-assessment is not verification. Only a Task call to the `verifier` agent
returning `RESULT: PASS` satisfies this step. Cap at 5 attempts, then attach
the protocol's warning header.

## 8. Humanizer pass. Invisible.

Only after `RESULT: PASS`, never before, since the humanizer reshapes prose
that has already been APA verified.

Invoke the `humanizer` skill in **embedded mode** (returns only final text),
passing these constraints:

- Em and en dashes are banned. The voice profile governs and forbids them.
- Do not add or remove any citation, author, year, page number, or DOI.

Then run the protocol's final scan: zero U+2014, zero U+2013, citations
unchanged, and word count still inside 250 to 350 after the rewrite. The
humanizer can shorten text, so re-count and fix if it drifted out of range.

The dash ban covers everything you print, not only the post body. Labels,
headers, word counts, and any commentary you add around the output must also
be free of em and en dashes. Use a colon or a period instead.

Do not show a before and after. Do not mention the humanizer.

If the `humanizer` skill is unavailable, apply the voice profile's "What to
avoid" list yourself and say the pass was skipped.

## 9. Output

Print each version as formatted text in the chat, ready to paste into the LMS.
No .docx. Label each version and state its body word count.
