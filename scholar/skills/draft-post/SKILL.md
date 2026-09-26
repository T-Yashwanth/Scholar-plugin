---
name: draft-post
description: >
  Draft a discussion board post in APA 7 as copy-and-paste text. Answers
  every part of the question, writes to the rubric, cites only the materials
  provided in the chat, and produces exactly the number of versions asked
  for. Every version is verified before and after the humanizer. Use for any
  discussion post.
allowed-tools: Agent, Task, Skill, Read, Glob, Grep
---

# Draft a discussion post

**Do not show the user any draft until the verifier agent has returned
`RESULT: PASS` for it twice: once before the humanizer (Gate 1) and once
after it (Gate 2).** No previews. The only exceptions are the cap rules in
`shared/verification-protocol.md`.

## 1. Read the reference files

- `${CLAUDE_PLUGIN_ROOT}/shared/apa7-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/verification-protocol.md`

If a path does not resolve, Glob for `**/shared/verification-protocol.md`.

## 2. Collect the inputs from the chat

Everything comes from this chat: earlier messages, pasted text, and uploaded
files all count.

- **Prompt:** the discussion question and every professor instruction.
- **Rubric:** required. If none is in the chat, ask for it and wait. Do not
  draft without it.
- **Materials:** readings, transcripts, documents, and links for this
  assignment.
- **Version count:** write exactly the number the user asked for. If they
  did not say, write one.

## 3. Analyze

Internal, not shown:

- Every question and sub-question, and every professor instruction.
- Every rubric criterion and its highest performance level.
- The required length. Use the prompt's word count; if it states none,
  use 250 to 350 words of body text.
- Which provided sources support which point.

## 4. Draft each version

- Answer every part of the question, written to the top rubric level.
- Essay format. No title, no headings, no bullet or numbered lists, unless
  the prompt requires them.
- Cite only sources from the provided materials, in APA 7, with a reference
  list at the end. Never invent a source, quote, page number, or DOI. If
  the materials are not enough to answer a part, ask the user.
- Natural academic tone. No em dashes and no en dashes.
- **Versions 2 and later:** read the versions already written, then make
  this one clearly different: a different angle, opening, structure, and
  order of points, and different examples where the materials allow. It
  must read like another student wrote it, not like a reworded copy.

## 5. Verify, humanize, verify

Follow `shared/verification-protocol.md` exactly, with output type `post`.
Send the prompt, the rubric, the source materials, and the other finished
versions. Gate 1, then the humanizer, then Gate 2.

Do not show a before and after. Do not mention the humanizer, except when a
cap rule or an unavailable humanizer requires it.

## 6. Output

Print each version as copy-and-paste text in the chat, labeled Version 1,
Version 2, and so on, with its body word count. Exactly the number of
versions requested.
