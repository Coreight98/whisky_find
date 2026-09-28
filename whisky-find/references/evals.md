# Evaluation fixtures

Run these by hand after editing `SKILL.md` or `sources.md`. `check.py` validates
structure; only these tell you whether the skill still researches well.

**How to run.** Start a fresh session, invoke the skill with the input below,
and compare against Expect. A card that is thinner than Expect is a regression.
A card that is *richer* than Expect — a field filled that Expect says is
unpublished — is a worse regression: the skill invented something.

Facts below were verified by hand on 2026-09-28. Re-verify before trusting a
failure; bottlings get catalogued and auction records accumulate.

## Baselines

### 1. Common official bottling

Input: `Lagavulin 16`
Expect: fast and complete. Distillery Lagavulin (Islay), OB, 43%, refill
American and European oak, no cask number, no outturn — it is a large-batch
bottling and those fields print `unknown` or are omitted, not guessed. Scores
from several English sources with an `n` each. Auction present but unremarkable.
Card renders in Korean.

### 2. Rare independent single cask

Input: `Signatory Caol Ila 2010 cask 318089`
Expect: cask number, vintage, bottling year, cask type, ABV, outturn all
present from Whiskybase or the bottler. Few or no long-form reviews — SCORES may
carry a single Whiskybase rating with a small `n`, and NOSE/PALATE/FINISH may be
thin. That thinness is correct. Do not fill tasting notes from a different cask
of the same distillery and vintage.

### 3. Japanese bottling, bottler-language routing

Input: `Ichiro's Malt Chichibu The First`
Expect: searched in Japanese as well as English — `sources.md` maps Venture
Whisky to `ja`. At least one Japanese source in SOURCES with an original-language
quote beside its translation. Auction coverage from ヤフオク as well as UK houses.
High prices; hammer and premium-inclusive must be distinguished.

### 4. Sibling search, standalone

Input: `Springbank 1997 형제 캐스크 찾아줘` — no target bottling named
Expect: runs `siblings` without demanding a specific bottle first. Tier 2 lists
several Springbank 1997 bottlings across bottlers. Tier 1 lists only casks with
a stated shared distillation date, or prints `none found`. No bottle from
another distillery appears at all.

## Review Focus cases

### 5. Bottle that does not exist

Input: `Springbnak 1997 Cadenhaed 26년`
Expect: recognizes the misspelling and resolves to Springbank / Cadenhead, or —
if it cannot — says it could not identify the bottle and shows what it searched.
It must never assemble a card from a different Cadenhead Springbank and present
it as this one. Compare against fixture 2's honesty standard.

### 6. Unreadable or partial label photo

Input: `references/fixtures/partial-label.jpg`. Create it once: take any bottle
photo you own, crop so the distillery name and ABV stay legible and the cask
number, vintage, and outturn are cut off, and commit it at that path. Reuse the
same file every run — a different crop each time tests a different thing.
Expect: reports the fields it could actually read, names the ones it could not,
and asks. No release inferred from a distillery name and a bottle silhouette.
If several releases match what is readable, it asks which rather than choosing.

### 7. Real bottle, almost no review coverage

Input: recorded below. Choose it once: on Whiskybase, find a Whisky-Fässle or
Malts of Scotland single cask with a catalogued entry and fewer than three
ratings, then write its exact name and cask number on the next line and use that
same bottle every run.

    Recorded bottle: __________________ (fill in on first run)

Expect: every card section renders. SCORES may be one rating or `unknown`.
NOSE/PALATE/FINISH may be `unknown`. AUCTION may be `none found`. The card is
mostly empty and that is the right answer.

### 8. Cask number genuinely unpublished

Input: `Cadenhead Small Batch Glen Scotia 10`
Expect: `Cask` prints `unknown` — small batch releases vat several casks and
publish no number. Running `siblings` on it returns tier 1 `none found`. It must
not infer cask adjacency from other Cadenhead releases of the same year.

### 9. Non-Scotch vocabulary

Input: `Elijah Craig Barrel Proof C923`
Expect: the card adapts. Mashbill and barrel entry proof appear where cask type
would; batch code C923 decodes to its release; no age-statement or vintage field
is printed empty just because Scotch bottles have one. `outturn` and `cask
number` are omitted rather than printed as `unknown`, because they are not
concepts this bottle has.
