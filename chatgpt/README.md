# Scholar for ChatGPT

The same Scholar workflow as the Claude plugin, packaged as a ChatGPT custom
GPT. It writes APA 7 papers as Word files, discussion posts, and replies to
classmates, and checks every output before and after a humanizer pass.

Nothing here changes the Claude plugin in `scholar/`. The APA rules and the
Word script are shared: you upload the same files from `scholar/`, so there
is one copy of each to maintain.

## What you upload

| File | Where it comes from | What it does |
|---|---|---|
| `instructions.txt` | `chatgpt/` | Pasted into the GPT's Instructions box |
| `scholar-playbook.md` | `chatgpt/knowledge/` | The paper, post, and reply workflows and the gates |
| `verifier-checks.md` | `chatgpt/knowledge/` | The four checks and the PASS/FAIL format |
| `humanizer-rules.md` | `chatgpt/knowledge/` | The humanizer pass, built in |
| `apa7-rules.md` | `scholar/shared/` | Full APA 7 reference |
| `apa7-checklist.md` | `scholar/shared/` | Short APA 7 checklist |
| `generate-docx.py` | `scholar/scripts/` | Makes the APA 7 Word file |

## Set up a custom GPT

Creating a GPT needs a paid ChatGPT plan.

1. In ChatGPT, open **Explore GPTs**, then **Create**, then the
   **Configure** tab.
2. **Name:** `Scholar`. **Description:** `APA 7 papers, discussion posts,
   and replies for DBA coursework.`
3. **Instructions:** paste the whole of `chatgpt/instructions.txt`.
4. **Knowledge:** upload the six files from the table above (everything
   except `instructions.txt`).
5. **Capabilities:** turn on **Code Interpreter & Data Analysis**. It runs
   the Word script and does the word counts and the dash scan. Turn
   **Web Search** off, so it cannot pull in sources you did not give it.
6. Optional conversation starters:
   - `Write the paper, 3 variants`
   - `Write the discussion post`
   - `Write me 2 replies`
7. Click **Create** and choose **Only me** (or share the link with the
   people who use it).

To update later, edit the GPT and replace the changed files.

## Set up a ChatGPT project instead

If you would rather not make a GPT, a project works too.

1. Create a project named `Scholar`.
2. In the project's instructions, paste `chatgpt/instructions.txt`.
3. Add the six knowledge files to the project's files.

If ChatGPT says it cannot find `generate-docx.py` when it is time to make
the Word file, upload the script into that chat and ask it to continue.

## Codex (OpenAI's coding agent)

ChatGPT custom GPTs and projects are set up in the ChatGPT website, so they
need no manifest file. Codex is different: it loads plugins from a
`.codex-plugin/plugin.json` manifest, the same way Claude loads
`.claude-plugin/plugin.json`. `scholar/.codex-plugin/plugin.json` points
Codex at the same `scholar/skills/` folder.

The skills were written for Claude, so in Codex two parts may not work as
written. They call the `scholar:verifier` agent and the `humanizer` plugin,
and they read files through `${CLAUDE_PLUGIN_ROOT}`. The skills already
search for the shared files when that path does not resolve. For the full
workflow in ChatGPT itself, use the custom GPT above.

## How to use it

The same way as in Claude. In one chat per subject (or per person), paste
the prompt, rubric, readings, and title page details, then ask in plain
words:

| You say | What it does |
|---|---|
| "Write the paper, 3 variants" | Paper workflow, three Word files to download |
| "Write the discussion post" | Post workflow, copy-and-paste text |
| "Write me 2 replies" (with classmates' posts pasted) | Reply workflow, two replies |

It follows the same rules as the Claude plugin: it asks for the rubric if
it is missing, cites only what you gave it, writes exactly the number you
asked for, and never uses em or en dashes.

## Differences from the Claude plugin

- **Verifier.** In Claude, the verifier is a separate agent with its own
  clean context. ChatGPT custom GPTs have no sub-agents, so the same model
  switches into a strict reviewer role for each gate. The checks are the
  same, and the counts and the citation compare run in Code Interpreter,
  but it is still the writer checking its own work. Read the output before
  you submit it.
- **Humanizer.** Claude uses the separate `humanizer` plugin. Here the
  rules are built in, in `humanizer-rules.md`, so there is nothing extra to
  install.
- **Word files.** Made in ChatGPT's Code Interpreter and given to you as
  download links, instead of being saved to a folder on your computer. The
  sandbox already has `python-docx`, so there is nothing to install.
- **Slash commands.** There are none. Ask in plain words, or name the
  workflow: "Use the paper workflow for this."

## Limits

- The checks are instructions the model follows, not code that forces them.
- Long chats get summarized. Paste key feedback or instructions again if a
  chat has run for a long time.
- Start a fresh chat for each new assignment, with only that assignment's
  prompt, rubric, readings, and any feedback you want applied.

## Files

    scholar/.codex-plugin/plugin.json   Codex manifest (see "Codex" above)

    chatgpt/
    ├── README.md                    this file
    ├── instructions.txt             paste into the GPT's Instructions box
    └── knowledge/
        ├── scholar-playbook.md      workflows, gates, Word file steps
        ├── verifier-checks.md       the four checks and the verdict format
        └── humanizer-rules.md       the built-in humanizer pass
