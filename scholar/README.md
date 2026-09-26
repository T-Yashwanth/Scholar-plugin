# Scholar

Academic writing assistant for DBA coursework. Writes APA 7 papers as Word
files, discussion posts, and replies to classmates. Every output is checked
before and after the humanizer, and you only see work that passed.

Scholar keeps no files and no memory of its own. Everything comes from the
chat you are in: the prompt, rubric, readings, title page details, and any
feedback you paste. Use one chat per subject, or per person.

## Requirements

- Python 3 on PATH as `python`, with `python-docx` installed
  (`python -m pip install python-docx`). Only papers need it.
- The [`humanizer`](https://github.com/blader/humanizer) plugin. Without it
  Scholar still works and tells you the humanizer pass was skipped.

## Install

The [Scholar-plugin](https://github.com/T-Yashwanth/Scholar-plugin) repo is
itself a marketplace named `scholar-plugin`. In a terminal:

    claude plugin marketplace add T-Yashwanth/Scholar-plugin
    claude plugin install scholar@scholar-plugin

Then reload Claude.

## How to use it

1. Start a chat for the subject. Give the title page details (name, school,
   course, instructor) for each person early on if you will need papers.
2. Paste or upload the prompt, the rubric, and the readings.
3. Ask in plain words:
   - "Write the paper, 3 variants" gives 3 Word files.
   - "Write the discussion post" gives copy-and-paste text.
   - "Write me 2 replies" (with classmates' posts pasted) gives 2 replies.
4. Claude asks only for what is missing, such as the rubric or the due date.

| Skill | For | Needs | Gives |
|---|---|---|---|
| `draft-essay` | Papers | Prompt, rubric, readings, title page details | One .docx per variant |
| `draft-post` | Discussion posts | Prompt, rubric, readings | Copy-and-paste text |
| `reply` | Replies to classmates | Classmates' posts | Exactly N replies |

## Rules it follows

- **Every part answered.** Each question, sub-question, and professor
  instruction is treated as a checklist item.
- **Rubric.** Required for papers and posts. Every criterion must be met at
  its highest level.
- **Length.** The professor's word count. Defaults only when the prompt
  gives none: posts 250 to 350 words, replies 100 to 130.
- **Sources.** Only the materials you provided in the chat. Nothing is
  invented; the checker confirms each citation against your materials.
- **Exact counts.** 3 variants means 3. 2 replies means 2.
- **Variants.** Each one is written to read like a different student:
  different angle, opening, structure, and order of points.
- **Replies.** Start with the student's full name and a comma, engage that
  student's actual points, professional tone. No citation or closing
  question unless the professor requires one. If you paste more posts than
  replies requested, Claude picks the posts with the most substance and
  says which.
- **No em dashes or en dashes** anywhere.

## Checking

    draft -> Check 1 -> humanizer -> Check 2 -> output

The `verifier` agent checks each draft and answers PASS or FAIL:

1. Every part of the question answered and every instruction followed.
2. Every rubric criterion at its highest level (skipped for replies).
3. APA 7 citations and references correct, and every source found in your
   materials.
4. Length, format, and title page right, and not a copy of another version.

Check 1 allows 5 attempts. Check 2 runs the same checks on the humanized
text and allows 3 attempts, using small fixes only. If Check 1 still fails,
you get the draft with a warning listing what is wrong. If Check 2 still
fails, you get the Check 1 version, which passed, marked as not humanized.

These checks are instructions to Claude, not code that forces them.

## Files

    scholar/
    ├── .claude-plugin/plugin.json
    ├── agents/verifier.md               the checker
    ├── scripts/generate-docx.py         APA 7 Word file writer
    ├── shared/
    │   ├── apa7-rules.md
    │   └── verification-protocol.md     the check, humanize, check order
    └── skills/
        ├── draft-essay/{SKILL.md,reference.md}
        ├── draft-post/SKILL.md
        └── reply/SKILL.md
