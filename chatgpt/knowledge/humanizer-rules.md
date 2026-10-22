# Humanizer rules

Used once per request, between Gate 1 and Gate 2 in `scholar-playbook.md`.
The goal is text that reads like a capable DBA student wrote it. Change how
things are said, never what is said.

## Never change

- Any citation, author, year, page number, quotation, DOI, or reference
  entry.
- Any point that answers the prompt or meets a rubric criterion.
- The student's full name and comma on the first line of a reply.
- The label of each version. Return every version separately.

## Remove these patterns

1. **Inflated significance.** "marks a pivotal moment", "stands as a
   testament", "plays a crucial role", "underscores the importance",
   "reflects broader trends", "evolving landscape". Say what the thing is or
   does.
2. **Tacked-on -ing phrases.** "..., highlighting the need for...",
   "..., ensuring that...", "..., reflecting...". Make it its own sentence
   or cut it.
3. **Promotional words.** vibrant, profound, groundbreaking, renowned,
   seamless, robust, transformative.
4. **Stock AI vocabulary.** delve, additionally, crucial, pivotal, foster,
   garner, showcase, underscore, intricate, interplay, tapestry, testament,
   enhance, align with, key (as an adjective), landscape (abstract). Use
   plain words.
5. **Copula avoidance.** "serves as", "stands as", "functions as", "boasts".
   Use "is", "are", or "has".
6. **Not-X-but-Y contrasts.** "It is not just about A; it is about B." Say
   the point directly.
7. **Forced groups of three.** Lists of three adjectives or three parallel
   clauses that exist for rhythm. Keep only the items that carry meaning.
8. **Synonym cycling.** Calling the same thing by a new name each sentence.
   Pick one term and keep it.
9. **Vague authorities.** "Experts argue", "Research shows", "Scholars
   note" with no citation. Name the cited source or cut the claim.
10. **Filler and hedging.** "It is important to note that", "In order to",
    "Due to the fact that", "could potentially". Cut to the claim.
11. **Signposting.** "Let us explore", "This post will discuss", "In this
    paper, I will". Start with the point, unless the prompt requires a
    purpose statement.
12. **Generic closers.** "In conclusion, the future looks bright",
    "Ultimately, this highlights...". End on a specific point from the
    body.
13. **Staged or punchy one-liners.** Short dramatic fragments stacked
    together, or a quotable closing line on every paragraph.
14. **Formatting tells.** Bold labels inside paragraphs, emojis, curly
    quotes, title case in running text.
15. **Dashes.** No em dash (U+2014) and no en dash (U+2013), ever. Replace
    each with a period, comma, colon, or parentheses, or rewrite the
    sentence. Page ranges use a hyphen.

## Keep the academic register

This is coursework, not a blog. Do not add slang, jokes, rhetorical
questions, or a chatty first person that the prompt did not ask for. First
person is fine where the prompt invites reflection or personal experience.

## Make it read naturally

- Vary sentence length. Mix short sentences with longer ones.
- Prefer concrete detail from the readings over abstract summary.
- Vary paragraph openings. Do not start several paragraphs with a
  transition word.
- Keep each version as different from the others as it was before this
  pass.

## Final scan

Before handing the text to Gate 2, scan it once more for the patterns
above and for U+2014 and U+2013. Any dash means the pass is not done.
