---
name: whisky-find
description: Identify and research a specific whisky — official bottling, independent bottling, or single cask — from a name, a label photo, or an auction lot. Searches English, the bottler's own language, and the user's language, then returns one card with cask facts, aggregated scores, translated tasting notes, auction prices, and explicit conflicts. Also searches sister casks from the same distillate. Use when the user names a bottle, shows a bottle photo, pastes an auction listing, or asks what a whisky is, how it tastes, what it is worth, or what else came out of that vintage. Do not use for cocktail recipes, bar recommendations, or suggesting what whisky to buy.
---

# whisky-find

Identify the bottle in front of the user, then say what it is, how it is
reviewed, and what it costs. Two operations share one front end.

**`lookup`** (default) — what is this bottle, how does it taste, what is it
worth. Produces the card.

**`siblings`** — what else came out of the same distillate. Produces the sister
cask list. Runs only when asked.

Nothing is stored. Every invocation researches from scratch.

## Identify the bottle

Resolve the input into one bottling before searching anything. Three inputs, one
identity.

**Text** — parse into distillery, age, vintage, bottler, series, cask number.
Accept misspellings and partial names; whisky names are hard to type.

**Photo** — read the label. Extract distillery, bottler, series, vintage, age,
ABV, cask number, outturn, bottle number. Copy any non-Latin text verbatim
before translating it: Japanese, Chinese, and Gaelic label text often carries
the cask detail. Report which fields you could actually read and which you could
not. Never infer the release from a distillery name and a bottle silhouette — if
the label is partial or blurred, say what you have and ask.

**Auction lot** — a URL or a screenshot. Parse lot title, images, stated
condition, fill level, and estimate, then research the bottling itself. The lot
description is a weak source for facts; see Trust rules.

**Classify the bottling.** Official bottling, independent bottling, or a
retailer, importer, or festival selection. The third is not an independent
bottling: the producer stays the brand, there is no bottler, and the program
name is an edition. Getting this wrong sends you hunting a bottler that does not
exist.

**Disambiguate before spending a search.** If the identity resolves to more than
one release — "Springbank 12 Cask Strength" spans a dozen batches — ask which
one. One question is cheaper than researching the wrong bottle.

**If you cannot identify it**, say so and show what you searched. Do not
assemble a card from a bottling that merely resembles the request.

## Language routing

Search three language sets for every lookup:

1. **English** — always.
2. **The bottler's or producer's home language** — look it up in
   `references/sources.md`.
3. **The user's language** — Korean by default.

For a retailer, importer, or festival selection, also search the destination
market's language; `references/sources.md` lists these patterns.

Report in the user's language. Whisky terms normally left in English stay in
English: peat, sherry butt, cask strength, NCF.

## lookup

What is this bottle, how does it taste, what is it worth.

**`lookup` never searches for sister casks**, at any depth. That is the
`siblings` operation, and the user asks for it separately.

Read `references/sources.md` for where to look. Fetch facts and opinions from
different tiers; never read a forum for an ABV.

Render exactly this card, in this section order, every time:

```
Springbank 1997 / 26y - Cadenhead (IB)
----------------------------------------
Distillery  Springbank (Campbeltown)
Bottler     Cadenhead's, Authentic Collection
Cask        Refill sherry hogshead, 1997->2023
ABV 49.2% / outturn 234 / NCF, no colour
Price       ~GBP450 retail

SCORES  Whiskybase 89.1 (n=41) / Whiskyfun 90
        r/Scotch ~88 (n=6)

NOSE    dried fig, wet rope, struck match
PALATE  oily, salted dark chocolate, brine
FINISH  long, smoky, mineral

AUCTION
  Live   2 lots - Whisky Auctioneer, closes 2026-10-04
                - ヤフオク, closes 2026-09-30
  Past   GBP 620-810 hammer over 7 results
         (2024-2026), trending up
         +10% buyer's premium -> ~680-890 paid
  (as of 2026-09-28)

! CONFLICTS
- Cask type: Whiskybase says refill sherry;
  label says bourbon. Label wins.
- JP reviews avg 91, EN avg 88.
- Cask number not published for this release.

SOURCES
- whiskybase.com/... (en)
- nomunication.jp/... (ja) "潮っぽい..."
- whiskyfun.com/... (en)
- whiskyhunter.net/... (en)

Ask for sister casks to search the 1997 vintage.
```

Every section prints even when empty: `unknown` for a missing field, `none
found` for an empty list. A thin card is a correct answer for an obscure bottle.

**Non-Scotch bottles.** The field names above are Scotch-shaped. Bourbon has a
mashbill, a barrel entry proof, and often no age or vintage; Japanese and
Taiwanese whiskies may have neither cask number nor outturn. Relabel or omit the
fields that do not apply. Do not print empty Scotch fields on a bourbon.

**Timestamp live lots.** They change hourly. The card says when it looked; it
does not promise the lot is still open.

## siblings

## Trust rules

**Conflict hierarchy**, applied in this order:

    bottle label / bottler > Whiskybase > retailer & auction > forum & blog

The winner fills the field. The conflict is *also* printed in CONFLICTS. Both,
always — a silently resolved conflict looks like a fact.

**Never invent.** A missing field prints `unknown`. A rare single cask with no
published cask number is a correct answer, not a failure to be papered over.

**Never average across scales.** Whiskyfun's /100 and a blog's five stars are
reported separately, each with its own `n`. When regional averages diverge
meaningfully — JP reviewers at 91, EN at 88 — that split goes in CONFLICTS.

**Label what a price is.** Retail, auction hammer, and premium-inclusive are
three different numbers. Never present one as another. When the buyer's premium
rate is unknown, report hammer only and say the real cost is higher.

**Quote originals.** A non-English tasting note keeps a short original-language
quote beside its translation in SOURCES.

## Depth

The user chooses, per query.

- **fast** (default) — one pass, roughly four to six sources, English plus the
  bottler's language.
- **deep** — on request, or when the user asks about a rare single cask.
  Parallel searches per language, forum archives, full auction history.

Depth applies to whichever operation is running. It does not make `lookup`
search for siblings.
