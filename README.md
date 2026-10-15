# whisky-find

A [Claude Code](https://claude.com/claude-code) skill that identifies a specific
whisky — official bottling, independent bottling, or single cask — from a name,
a label photo, or an auction lot, and reports what it is, how it reviews, and
what it costs.

It searches three language sets every time: English, the bottler's own language,
and yours. Reviews of a Japanese bottling live in Japanese; an English-only
search quietly misses them.

## Two operations

**`lookup`** (default) — what is this bottle, how does it taste, what is it
worth. Renders one card.

**`siblings`** — what else came out of the same distillate, split into true
sister casks and same-distillery/same-vintage bottlings. Runs only when asked.

## The card

```
Springbank 1997 / 26y - Cadenhead (IB)
----------------------------------------
Distillery  Springbank (Campbeltown)
Bottler     Cadenhead's, Authentic Collection
Cask        Refill sherry hogshead, 1997->2023
ABV 49.2% / outturn 234 / NCF, no colour
Price       ~GBP450 retail

SCORES  Whiskybase 89.1 (n=41) / Whiskyfun 90 (n=1)
        r/Scotch ~88 (n=6)

NOSE    dried fig, wet rope, struck match
PALATE  oily, salted dark chocolate, brine
FINISH  long, smoky, mineral

AUCTION
  Live   2 lots - Whisky Auctioneer, closes 2026-10-04
  Past   GBP 620-810 hammer over 7 results, trending up
         (as of 2026-09-28)

! CONFLICTS
- Cask type: Whiskybase says refill sherry;
  label says bourbon. Label wins.

SOURCES
- whiskybase.com/... (en)
- nomunication.jp/... (ja) "潮っぽい..."
```

Every section prints even when empty — `unknown` for a field, `none found` for a
list. A thin card is the correct answer for an obscure bottle.

## What it will not do

- **Never invent a field.** No cask number published means `unknown`, not a
  plausible number.
- **Never average across scales.** Whiskyfun's /100 and a blog's five stars stay
  separate, each with its own `n`.
- **Never silently resolve a conflict.** Label beats Whiskybase beats retailer
  beats forum — and the conflict still prints.
- **Never recommend.** It identifies and prices the bottle you named. Which
  bottle you should buy is not its call.
- **Never cross distilleries** in `siblings`, however good the taste match —
  same ownership included.
- **Notes come from the identified bottling only.** A note about a different
  batch is not evidence about this one. That is the most convincing way a card
  can be wrong: nothing invented, a real source cited, still another bottle.

## Install

Copy the skill into your skills directory:

```bash
cp -r .claude/skills/whisky-find ~/.claude/skills/   # user-wide
# or leave it in .claude/skills/ of a project
```

Then just name a bottle, paste an auction lot, or show a label photo.

## Checks

```bash
python3 .claude/skills/whisky-find/check.py
```

Structural only: frontmatter, required sections, source-table shape. Whether a
card is any good is checked by hand against
[`references/evals.md`](.claude/skills/whisky-find/references/evals.md).

## Layout

```
.claude/skills/whisky-find/
  SKILL.md               the skill itself
  check.py               structural checks
  references/
    sources.md           bottler languages, source tiers, auction houses
    evals.md             hand-run evaluation fixtures
```
