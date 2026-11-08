---
name: consolidate-notes
description: Consolidate algorithm notes into one topic reference, or format a topic note in this repository's style, with shared pseudocode templates and compact problem lists.
---

# Consolidate notes

Use the style established by `Monotonic Structures/Monotonic Stack.mdx` and
`Monotonic Structures/Monotonic Deque.mdx`. The structure below captures the
preferred format, including omitting “When To Use” headings.

## Note structure

Create `<Topic>.mdx` alongside the original base note, using the topic name
without “Base”. Keep one frontmatter block, preserve the base note's date and
other relevant metadata, and update its title.

Use this outline. Bracketed text describes content to supply; omit sections
that have no source material rather than inventing content to fill them.

````mdx
---
title: "Topic"
date: 18Jul26
---

# Topic

[Short introduction explaining what the technique is useful for.]

## Template

[Core reasoning and shared template. Use multiple named template sections
or implementation subsections when the base note needs them.]

```python
for i in scan order:
    while candidates and current makes last candidate unnecessary:
        remove last candidate

    use best candidate if present
    add i
```

[Existing mental model, diagram, or caveat where it helps.]

## Problems

**Optional problem group**

- [Problem title](https://leetcode.com/problems/problem-slug/description/)
  - key observation, formula, or constraint worth remembering
- [Another problem](https://leetcode.com/problems/another-slug/description/)

---

# Some generalised variations

## Pattern name

[Introduce the pattern directly, without a “When To Use” heading.]

### Template

```python
for item in sequence:
    maintain candidates for this pattern
    update answer
```

[Brief explanation or caveat if needed.]

### Problems

- [Problem title](https://leetcode.com/problems/problem-slug/description/)
  - what changes for this problem

---

## Another pattern

[Repeat the pattern structure.]
````

## Content and formatting

- Start with the base explanation and shared templates, then append general
  practice problems, then the pattern sections. Keep the existing pattern
  order unless the user requests a different order.
- Use `#` for the topic and “Some generalised variations”, `##` for base
  sections and individual patterns, and `###` for sections within a pattern.
  Separate patterns with `---`.
- Remove “When To Use” headings at every level, keeping their text directly
  beneath the topic or pattern heading.
- Highlight shared pseudocode with `python`. Mix Python syntax and plain
  English where useful; do not turn templates into complete implementations.
- Problems are bullet lists, with short sub-bullets only where details help.
  Keep useful observations, formulas, constraints, and duplicate-handling hints.
  Use bold labels for problem groups when needed, rather than a heading per problem.
- Use descriptive problem links when available. Preserve non-LeetCode or
  unlinked exercises; do not invent links or replace them with unrelated problems.
- Remove problem-specific solution code and repetitive “Problem”, “Pattern”,
  and “Applied pseudocode” labels. Condense their useful details into hints.
- Preserve the user's voice and useful explanations, images, and caveats.
  Adapt the format without adding unsolicited lessons or rewriting algorithms.

## Merge and cleanup

1. Read the base, practice, pattern, and index notes for the requested topic.
   Inventory their problems and assets so useful material survives the merge.
   An index that only introduces the folder does not need its own section.
2. Create the combined note as a copy. Keep the originals intact for review;
   do not rename or delete them during the initial merge.
3. Check that all problems and useful details survived, only one frontmatter
   block remains, headings follow the outline, and code fences are balanced.
   Problems sections must contain no solution code blocks. Update relative
   image and document links for the combined note's location, and remove
   redundant prerequisite links to material now included in the same note.
4. When cleanup is requested, list the exact original files proposed for
   deletion, including base, practice, pattern, and folder index notes as
   applicable. Get confirmation of that list unless it is already authorized.
   Preserve the combined note and all assets it still uses.
5. After authorized deletion, remove empty topic folders and update any local
   links or navigation entries pointing to the deleted originals. Report what
   was removed and anything that could not be checked.
