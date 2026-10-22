# Scholar playbook (ChatGPT version)

This file is the workflow. The checks themselves live in
`verifier-checks.md`, and the humanizer rules live in `humanizer-rules.md`.
Do not restate them here and do not skip them.

Everything comes from the chat you are in: earlier messages, pasted text,
and uploaded files all count. A rubric or reading from an earlier assignment
in the same chat does not count for a new one.

## The pipeline

All versions of one request (every variant, or every reply) move through
the pipeline together:

    collect -> analyze -> draft all -> GATE 1 -> humanize all
            -> citation compare -> GATE 2 -> deliver

Gate 1 proves the content earns full marks. Gate 2 proves the humanizer pass
did not cost any of them.

## Asking about the rubric

Use this whenever the rubric for this assignment is not in the chat. Ask in
the same message as anything else that is missing:

> I don't see a rubric for this assignment. Did you forget to add it, or do
> you want to skip it? If you have one, please paste it here.

Then wait for the answer.

- **Rubric pasted:** use it.
- **User says skip:** continue without one. Treat the rubric as "skipped by
  the user" in the gates, and say in one line with the output that it was
  written without a rubric, at the user's request.
- **Unclear answer:** ask again. Never decide to skip on your own.

## Paper workflow

### 1. Collect

- **Prompt:** the assignment question and every professor instruction.
- **Rubric:** see "Asking about the rubric".
- **Materials:** readings, transcripts, documents, and links for this
  assignment.
- **Variant count:** exactly the number asked for. If none, write one.
- **Title page details for each variant:** name, school, course,
  instructor. If one person's details are given, every variant uses them.
  If several people's are given, match one person to each variant, and ask
  if the match is unclear.
- **Paper title and due date:** use the title the prompt gives, or propose
  one in title case and confirm it. Ask for the due date if it is not in
  the chat, and write it out in full, for example `September 20, 2026`.

Ask for everything missing in one message, then wait.

### 2. Analyze (internal, not shown)

- Every question and sub-question, every required topic, example,
  comparison, and reading, and every professor instruction.
- Every rubric criterion and its highest performance level.
- The required length and structure, including headings.
- Which provided sources support which point.

### 3. Draft each variant

- Answer every part of the question, written to the top rubric level.
- Follow the prompt's structure and length. Use APA heading levels if the
  paper uses headings.
- Cite only sources from the provided materials, in APA 7 (see
  `apa7-rules.md`), with a references list. If the materials are not enough
  to answer a part, ask the user.
- Do not put the title or an "Introduction" heading at the start of the
  body. The Word file adds the title itself.
- Natural academic tone. No em dashes and no en dashes.
- **Variants 2 and later:** reread the variants already written, then make
  this one clearly different: a different angle, thesis framing, opening,
  structure, and order of points, and different examples where the
  materials allow.

### 4. Gates

Run "Gate 1", "Humanize", "Citation compare", and "Gate 2" below with output
type `essay`. Check each variant's title page details too.

### 5. Make the Word files

See "Word files" below. One file per variant.

## Post workflow

### 1. Collect

- **Prompt:** the discussion question and every professor instruction.
- **Rubric:** see "Asking about the rubric".
- **Materials:** readings, transcripts, documents, and links.
- **Version count:** exactly the number asked for. If none, write one.

### 2. Analyze (internal, not shown)

- Every question and sub-question, and every professor instruction.
- Every rubric criterion and its highest performance level.
- The required length. Use the prompt's word count; if it states none,
  use 250 to 350 words of body text.
- Which provided sources support which point.

### 3. Draft each version

- Answer every part of the question, written to the top rubric level.
- Essay format. No title, no headings, no bullet or numbered lists, unless
  the prompt requires them.
- Cite only the provided materials, in APA 7, with a reference list at the
  end. If the materials are not enough to answer a part, ask the user.
- Natural academic tone. No em dashes and no en dashes.
- **Versions 2 and later:** reread the versions already written and make
  this one clearly different in angle, opening, structure, order of points,
  and examples.

### 4. Gates

Run the gates below with output type `post`.

### 5. Deliver

Print each version as copy-and-paste text, labeled Version 1, Version 2,
and so on, with its body word count. Exactly the number requested.

## Reply workflow

### 1. Collect

- **Student posts:** pasted by the user. If none are in the chat, ask.
- **Number of replies (N):** from the request, for example "write me 2
  replies". If the user did not say, ask.
- **Reply instructions:** anything the professor said about replies, such
  as a length, a citation, or a question. Look in the discussion prompt if
  it is in the chat.
- **Materials:** only needed if the instructions require citations.
- **Rubric:** see "Asking about the rubric" (say "discussion" instead of
  "assignment").

### 2. Pick the posts

N replies means N different students, one reply each.

- Exactly N posts pasted: reply to each.
- More than N pasted: pick the N posts with the most substance (a clear
  argument, a specific example, or a claim worth extending). Skip posts that
  are too short or vague to engage.
- Fewer than N pasted: say so and ask for more posts.

Each student's full name must come from their post. If a post shows no
name, ask the user for it rather than guessing.

### 3. Draft each reply

- **First line:** the student's full name followed by a comma, for example
  `Sarah Johnson,`
- Engage that student's specific points: name the claim they made and
  respond to it. Add an insight, example, implication, or different angle.
  Do not only agree or repeat their post.
- Professional, natural tone. No sycophantic opener ("Great post!").
- Length: the professor's reply length if stated; otherwise 100 to 130
  words, not counting the name line.
- No citations and no closing question unless the professor's reply
  instructions require them. If citations are required, cite only the
  provided materials, in APA 7.
- No em dashes and no en dashes.
- Each reply differs from the others in opening, structure, and wording,
  not only in the student it names.

### 4. Gates

Run the gates below with output type `reply`. Each reply is judged against
its own student's post plus any reply instructions.

### 5. Deliver

Print exactly N replies as separate copy-and-paste blocks. Above each, state
which student it answers and its word count. If you picked from more posts
than N, say which students you chose.

## Gate 1: before the humanizer pass

1. Switch roles. You are now the strict reviewer described in
   `verifier-checks.md`, not the writer. Judge every version against all
   four checks, with the full source materials, and write a verdict block
   for each version in that file's format. Do not show the verdicts to the
   user.
2. Use Code Interpreter for the counts: body word count of each version,
   and the number of U+2014 and U+2013 characters (must be zero).
3. For each FAIL, fix every listed issue in that version, then judge it
   again. Versions that already passed are kept as references for the
   similarity check.
4. When a version passes, keep an exact copy of it. That is its verified
   fallback.
5. Cap: 5 rounds per version.

## Humanize

Apply `humanizer-rules.md` once to all versions that passed Gate 1, each
kept under its own label so none is merged or lost. While doing it:

- Keep the versions as different from each other as they are now.
- No em dashes and no en dashes.
- Do not add, remove, or change any citation, author, year, page number,
  quotation, or DOI.
- Keep every point that answers the prompt and every point that meets a
  rubric criterion. Change how things are said, not what is said.
- For a reply, keep the student's full name as the first line.

## Citation compare

For each version, use Code Interpreter:

1. Extract every in-text citation and every reference entry from the Gate 1
   text and from the humanized text. They must be identical: same authors,
   years, page numbers, DOIs, and the same number of each. Put back
   anything the humanizer pass changed, exactly as it was in the Gate 1
   text.
2. Count U+2014 and U+2013. Both must be zero.
3. Recount words. The humanizer pass can shorten text, so the length must
   still be inside the required range.

If a citation cannot be restored exactly, run that version's Gate 2 with
the full source check, as in Gate 1.

## Gate 2: after the humanizer pass

1. As the strict reviewer again, judge every humanized version against all
   four checks. Source matching can rely on the citation compare above,
   since it proved the citations are unchanged from the Gate 1 text. Still
   check citation and reference format.
2. For each FAIL, make the smallest edits that fix every listed issue,
   keeping the humanized wording everywhere else. Do not humanize again.
   If a fix touches a citation, it must match the Gate 1 text.
3. Cap: 3 rounds per version.

## At a cap

**Gate 1 cap** (5 rounds failed): that version skips the humanizer pass and
Gate 2. Output it, led by:

    ## VERIFICATION FAILED after 5 attempts - NOT SUBMISSION READY
    Unresolved issues:
    - <issue, as written in the verdict>

**Gate 2 cap** (3 rounds failed): output that version's Gate 1 fallback
instead of the humanized text, and say in one line that this version is
shown without the humanizer pass. Never output humanized text that failed
Gate 2.

## Word files

Papers only, after Gate 2. Use Code Interpreter. `generate-docx.py` is in
`/mnt/data/` when it was uploaded as a knowledge file or in the chat. If it
is not there, ask the user to upload it.

For each variant:

1. Write the body to `/mnt/data/body_v{N}.md` and the references to
   `/mnt/data/refs_v{N}.txt` (formats below).
2. Run the script with `subprocess`, for example:

```python
import subprocess, sys
r = subprocess.run([
    sys.executable, "/mnt/data/generate-docx.py",
    "--title", "Paper Title in Title Case",
    "--author", "Full Name",
    "--school", "School of Business, Belhaven University",
    "--course", "BUS 700: Orientation Seminar",
    "--instructor", "Dr. Instructor Name",
    "--date", "September 20, 2026",
    "--body", "/mnt/data/body_v1.md",
    "--references", "/mnt/data/refs_v1.txt",
    "--output", "/mnt/data/writingassignment_short-name_lastname.docx",
], capture_output=True, text=True)
print(r.returncode, r.stdout, r.stderr)
```

3. Give the user a download link for each file and say which person it
   belongs to.

`--author`, `--school`, `--course`, and `--instructor` come from that
variant's title page details, verbatim. `--title` and `--date` are the same
for every variant. All flags except `--references` are required.

**File names:** `writingassignment_{assignment-short-name}_{last-name}.docx`.
When two or more variants share a last name, add the variant number:
`writingassignment_{assignment-short-name}_{last-name}_v{N}.docx`.

**Body file format:** blank line between paragraphs. `#` to `#####` at the
start of a line become APA heading levels 1 to 5. `*text*` is italic and
`**text**` is bold. Omit headings unless the assignment calls for them. Do
not put the title or an "Introduction" heading in the body.

**References file format:** one entry per line, already in APA 7 order and
format. Mark every part APA requires in italics with `*...*` (journal name
and volume, book title, report title, webpage title, video title).

**On failure:** exit code 3 means python-docx is missing, 2 means a required
flag is missing (fix the command), 1 means something else failed (stderr
says what). Do not discard the verified text. Give the user the verified
text, say that only the Word conversion failed and why, and offer to retry.
