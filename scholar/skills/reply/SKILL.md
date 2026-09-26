---
name: reply
description: >
  Write replies to classmates' discussion posts. "Write me N replies" gives
  exactly N replies, each to a different student, opening with the
  student's full name, professional and specific to that student's points.
  Every reply is verified before and after the humanizer. Use when the user
  pastes classmates' posts and asks for replies or responses.
allowed-tools: Agent, Task, Skill, Read, Glob, Grep
---

# Write replies to classmates

**Do not show the user any reply until the verifier agent has returned
`RESULT: PASS` for it twice: once before the humanizer (Gate 1) and once
after it (Gate 2).** The only exceptions are the cap rules in
`shared/verification-protocol.md`.

## 1. Read the reference files

- `${CLAUDE_PLUGIN_ROOT}/shared/apa7-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/verification-protocol.md`

If a path does not resolve, Glob for `**/shared/verification-protocol.md`.

## 2. Collect the inputs from the chat

- **Student posts:** pasted by the user. If none are in the chat, ask.
- **Number of replies (N):** from the request, for example "write me 2
  replies". If the user did not say, ask.
- **Reply instructions:** anything the professor said about replies, such
  as a length, a citation, or a question. Look in the discussion prompt if
  it is in the chat.
- **Materials:** the readings in the chat, only needed if the instructions
  require citations.

## 3. Pick the posts

N replies means N different students, one reply each.

- If exactly N posts were pasted, reply to each.
- If more than N were pasted, pick the N posts with the most substance to
  respond to: a clear argument, a specific example, or a claim worth
  extending. Skip posts that are too short or vague to engage.
- If fewer than N were pasted, say so and ask for more posts.

Each student's full name must come from their post. If a post shows no
name, ask the user for it rather than guessing.

## 4. Draft each reply

- **First line:** the student's full name followed by a comma, for
  example `Sarah Johnson,`
- Engage that student's specific points: name the claim they made and
  respond to it. Add value: an insight, example, implication, or a
  different angle. Do not only agree or repeat their post.
- Professional, natural tone. No sycophantic opener ("Great post!").
- Length: the professor's reply length if stated; otherwise 100 to 130
  words, not counting the name line.
- No citations and no closing question unless the professor's reply
  instructions require them. If citations are required, cite only the
  provided materials, in APA 7.
- No em dashes and no en dashes.
- Each reply must differ from the others in opening, structure, and
  wording, not only in the student it names.

## 5. Verify, humanize, verify

Follow `shared/verification-protocol.md` exactly, with output type `reply`.
For each reply, send the student's post and any reply instructions as the
prompt, the words "no rubric", the materials if the reply cites any, and
the replies already finished. Gate 1, then the humanizer, then Gate 2.

Do not mention the humanizer, except when a cap rule or an unavailable
humanizer requires it.

## 6. Output

Print exactly N replies as separate copy-and-paste blocks. Above each,
state which student it answers and its word count. If you picked from more
posts than N, say which students you chose.
