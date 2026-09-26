# Scholar

Academic writing assistant for DBA coursework. It writes:

- **Papers** as APA 7 Word (.docx) files
- **Discussion posts** as copy-and-paste text
- **Replies to classmates** as copy-and-paste text

Every output is checked before and after the humanizer, and you only see
work that passed.

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
itself a marketplace named `scholar-plugin`. Run these in a terminal, not in
the chat:

    claude plugin marketplace add T-Yashwanth/Scholar-plugin
    claude plugin install scholar@scholar-plugin

Then reload Claude. To get a newer version later:

    claude plugin marketplace update scholar-plugin

## What is inside

| Part | Kind | What it does |
|---|---|---|
| `draft-essay` | Skill | Writes papers and makes the Word files |
| `draft-post` | Skill | Writes discussion posts |
| `reply` | Skill | Writes replies to classmates |
| `verifier` | Agent | Checks one draft and answers PASS or FAIL. Never edits. |
| `generate-docx.py` | Script | Turns a finished paper into an APA 7 Word file |
| `apa7-rules.md` | Rules | APA 7 summary with sources and reference examples |
| `verification-protocol.md` | Rules | The check, humanize, check order |

A **skill** is a set of step-by-step instructions Claude follows. An
**agent** is a separate Claude with its own clean context, so it checks the
draft without the writer's assumptions.

## How it works automatically

You do not have to call anything by name. Ask in plain words, and Claude
picks the matching skill from its description:

| You say | Skill that runs |
|---|---|
| "Write the paper, 3 variants" | `draft-essay` |
| "Write the discussion post" | `draft-post` |
| "Write me 2 replies" (with classmates' posts pasted) | `reply` |

Once a skill runs, it does every step below by itself:

1. **Collect.** Reads the prompt, rubric, readings, and title page details
   from the chat. Asks only for what is missing, in one message.
2. **Plan.** Lists every question, sub-question, instruction, and rubric
   criterion as a checklist. Works out the required length.
3. **Write.** Drafts each version. From the second version on, it reads the
   earlier versions first so the new one is clearly different.
4. **Check 1.** Calls the `verifier` agent. Up to 5 attempts, fixing
   everything it reports each time.
5. **Humanize.** Calls the `humanizer` skill to make the text read
   naturally, without touching citations or dropping any point.
6. **Check 2.** Calls the `verifier` agent again on the humanized text. Up
   to 3 attempts, with small fixes only.
7. **Deliver.** Word files for papers (full paths shown), text for posts and
   replies. Exactly the number you asked for.

The verifier runs four checks each time:

1. Every part of the question answered and every instruction followed.
2. Every rubric criterion at its highest level (skipped for replies).
3. APA 7 citations and references correct, and every source found in the
   materials you gave in the chat.
4. Length, format, and title page right, and not a copy of another version.

If Check 1 still fails after 5 attempts, you get the draft with a warning
listing what is wrong. If Check 2 still fails after 3, you get the Check 1
version, which passed every check, marked as not humanized.

## Calling skills and agents yourself

Use this when you want a specific skill for sure, or want to run one step
on its own.

**A skill.** In Claude Code (the VS Code extension or the terminal), type a
slash command, with or without text after it:

    /scholar:draft-essay
    /scholar:draft-post
    /scholar:reply write me 2 replies

In any Claude chat, you can also ask for it by name:

    Use the scholar draft-post skill for this.

**The verifier on its own.** To check text you wrote or edited yourself,
ask:

    Use the scholar:verifier agent to check this post.

Give it the same things the skills do: the text, the prompt, the rubric (not
for replies), the readings it cites, and the type: essay, post, or reply.
It returns PASS or FAIL with a list of fixes. It does not rewrite anything.

**The humanizer on its own.** It comes from the humanizer plugin:

    /humanizer

Running a step by hand skips the rest of the flow. A draft you humanize
yourself is not checked again unless you then ask for the verifier.

## Rules it follows

- **Every part answered.** Each question, sub-question, and professor
  instruction is a checklist item.
- **Rubric.** Required for papers and posts. Every criterion must be met at
  its highest level.
- **Length.** The professor's word count. Defaults only when the prompt
  gives none: posts 250 to 350 words, replies 100 to 130.
- **Sources.** Only the materials you provided in the chat. Nothing is
  invented.
- **Exact counts.** 3 variants means 3. 2 replies means 2. If you give no
  number, it writes one.
- **Variants.** Each one reads like a different student wrote it: different
  angle, opening, structure, and order of points.
- **Title pages.** From the details you give in the chat. One person's
  details are used for every variant; several people's are matched one per
  variant.
- **Replies.** Start with the student's full name and a comma, engage that
  student's actual points, professional tone. No citation or closing
  question unless the professor requires one. If you paste more posts than
  replies requested, it picks the posts with the most substance and says
  which.
- **No em dashes or en dashes** anywhere. Page ranges use a hyphen.

## Limits

- The checks are instructions Claude follows, not code that forces them.
- Chats keep your materials, but very long chats get summarized. Paste key
  feedback or instructions again if a chat has run for a long time.

## Files

    scholar/
    ├── .claude-plugin/plugin.json
    ├── agents/verifier.md               the checker
    ├── scripts/generate-docx.py         APA 7 Word file writer
    ├── shared/
    │   ├── apa7-rules.md                APA summary, sources, examples
    │   └── verification-protocol.md     the check, humanize, check order
    └── skills/
        ├── draft-essay/{SKILL.md,reference.md}
        ├── draft-post/SKILL.md
        └── reply/SKILL.md
