# FitFindr

<!-- > ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go. -->

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr helps a user search for thrifted clothing based on a description, optional size, and maximum price. It searches available listings, selects a matching item, and suggests one or two outfits using pieces from the user's wardrobe. It then creates a short fit-card caption describing the selected item and the overall outfit vibe. If no listings match the search, the agent stops early and tells the user to try changing the description, size, or maximum price.

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->


### `search_listings`

- **What it does:** Searches the available listings for items matching the user's description and optional size and maximum price.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of matching listing dictionaries, ordered with the best matches first. Each dictionary contains the listing's id, title, description, category, style tags, size, condition, price, colors, brand, and platform.
- **When it has nothing:** Returns an empty list `[]` when no listings match. Size matching is case-insensitive and should allow combined sizes such as `S/M` to match `M` without treating arbitrary substrings such as `L` in `XL` as a match.

### `suggest_outfit`

- **What it does:** Uses the selected thrift listing and the user's wardrobe to generate one or two outfit suggestions.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing outfit suggestions based on the selected item and the user's saved wardrobe pieces.
- **When it has nothing:** If the wardrobe contains no items, returns general styling advice for the selected item instead of failing.

### `create_fit_card`

- **What it does:** Creates a short post-style caption using the outfit suggestion and selected thrift item.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A two-to-four sentence caption that mentions the item, its price and platform, and describes the outfit's vibe.
- **When it has nothing:** If `outfit` is empty or only whitespace, returns a descriptive message explaining that a fit card could not be created instead of raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
First, the agent parses the user's query and calls `search_listings` with the description, size, and maximum price. If `search_listings` returns an empty list, the agent saves a helpful message in the session telling the user to change their description, size, or maximum price, and then stops. Otherwise, the agent takes the first search result, saves it as the selected item, passes it to `suggest_outfit` along with the wardrobe.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
The query is parsed using regular expressions and string cleanup. The parser extracts a maximum price from phrases such as "under $30", extracts a size from phrases such as "size M", removes those constraints and common filler words, and uses the remaining text as the search description.


**What moves through the session:** <!-- which fields, in what order -->
The original query is stored in session["query"]. The parsed description, size, and maximum price are stored in session["parsed"], followed by the search results in session["search_results"]. If results exist, the first result is stored in session["selected_item"], the outfit suggestion is stored in session["outfit_suggestion"], and the final caption is stored in session["fit_card"]. If no results are found, session["error"] is set and the agent stops before the later tools run.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'looking for a vintage graphic tee under $30'

Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two outfit ideas using your new Y2K butterfly baby tee and pieces from your wardrobe:

**Outfit 1: Casual Y2K Streetwear**
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag
* **Why it works:** The tight, cropped fit of the baby tee balances out the voluminous silhouette of the baggy dark-wash jeans for an authentic 2000s streetwear look.

**Outfit 2: Grungy Contrast**
* **Outerwear:** Vintage black denim jacket
* **Bottoms:** Wide-leg khaki trousers
* **Shoes:** Black combat boots
* **Why it works:** Pairing the sweet, feminine butterfly graphic with heavy black combat boots and a dark denim jacket creates a cool high-low contrast that leans into the vintage-grunge aesthetic.

Fit card: The Y2K Baby Tee — Butterfly Print listed on depop for $18.0 channels a nostalgic 2000s streetwear vibe. It pairs effortlessly with baggy dark-wash jeans and chunky sneakers for a balanced silhouette. Alternatively, styling it with wide-leg trousers, a black denim jacket, and combat boots creates a cool, grungy high-low contrast.

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'},{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition':'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```text
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit ideas using your new vintage Levi's 501 jeans and pieces from your wardrobe:

**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* A classic denim-on-denim look balanced by a fitted tank and chunky sneakers for an effortless streetwear vibe.

**Outfit 2: Cozy & Classic**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Black combat boots
*   *Why it works:* Tucking the Levi's into the combat boots with a belt adds structure to the oversized grey crewneck, creating an easy, grunge-leaning casual outfit.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Nothing beats the timeless vibe of these Vintage Levi's 501 Jeans in a medium wash, listed on depop for $38.0. Paired with crisp white sneakers, the look leans into effortless streetwear and classic casual style. It is the ultimate laid-back uniform that works for literally any day of the week.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- What I asked for: Targeted help refining `search_listings` and checking its description, size, and price filters.

- What came back: Suggestions for keyword scoring and separate filters, including the size-matching edge case where a substring check could match `L` inside `XL`.

- What I changed: I reviewed and adjusted the suggestions before using them, keeping combined-size matches such as `M` in `S/M` while rejecting unrelated size substrings.

**Moment 2**

- What I asked for: Help improving the `create_fit_card` prompt after captions implied purchases or sounded like sales posts.

- What came back: Suggestions to keep captions factual, explicitly avoid wording such as "Scored this," and give a listing-based alternative.

- What I changed: I reviewed the wording and used a focused prompt change to avoid unsupported personal experiences and seller-style language, while retaining the price, platform, and length requirements.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

Results from `python run_eval.py --label before`, recorded in [run_2026-10-12_0102_before.md](results/run_2026-10-12_0102_before.md). Each scenario ran five times with caching off and temperature 0.9.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit with a helpful message | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected-item ID matches the item passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes price and platform and has 2–4 sentences | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every search result respects the maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

For criterion 4, sentence counts were 3, 2, 3, 2, and 3; all five captions included the selected item’s $15.0 price and depop platform. The empty-wardrobe scenario remains a separate diagnostic and is not one of these five criteria.

**Real output from one try per criterion**

The following excerpts are copied from Try 1 of each numbered scenario in the report. The report was produced by `run_eval.py::main` / `write_report`; trace lines were produced by `agent.py::run_agent` using `trace.py::step`.

**Criterion 1 — Try 1**

Query: `vintage graphic tee under $30`

Produced by `agent.py::run_agent`; caption returned by `tools.py::create_fit_card`.

```text
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    Matches found: select the first result. Returned IDs and prices: [('lst_002', 18.0), ('lst_006', 24.0), ('lst_033', 19.0), ('lst_015', 26.0), ('lst_017', 15.0), ('lst_003', 22.0), ('lst_011', 27.0), ('lst_012', 20.0), ('lst_013', 30.0), ('lst_014', 12.0)]
[3] select_item
      in:  First search result
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    session['selected_item'] ID: lst_002
[4] suggest_outfit
      in:  new_item ID: lst_002; wardrobe items: 10
      out: Here are two outfit ideas combining your new Y2K butterfly baby tee with pieces you already own:  **Outfit 1: …
      →    Used the selected item and saved wardrobe.
[5] create_fit_card
      in:  new_item ID: lst_002; outfit: Here are two outfit ideas combining your new Y2K butterfly baby tee with pieces …
      out: The Y2K Baby Tee — Butterfly Print listed on depop for $18.0 brings together sweet vintage graphics and effort…
      →    All three tools completed.
```

Fit card:

```text
The Y2K Baby Tee — Butterfly Print listed on depop for $18.0 brings together sweet vintage graphics and effortless cottagecore charm. Pairing the fitted graphic top with baggy dark wash denim or wide-leg khaki trousers creates a balanced look that leans into classic early-2000s streetwear and minimal earth tones. Complete with chunky white sneakers and a brown leather belt, the finished outfit effortlessly merges nostalgic style with everyday casual wear.
```

**Criterion 2 — Try 1**

Query: `designer ballgown size XXS under $5`

Produced by `agent.py::run_agent`; stopped-session fields printed by `run_eval.py::write_report`.

```text
- stopped early: yes — I couldn't find any matching listings. Try changing the description, size, or maximum price.
- selected_item: (none)
- search_results: 0

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    No matches: stop before suggest_outfit and create_fit_card.
```

**Criterion 3 — Try 1**

Query: `vintage graphic tee under $30, size M`

Produced by `agent.py::run_agent`, showing the session-selected ID and the input to `tools.py::suggest_outfit`.

```text
[3] select_item
      in:  First search result
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    session['selected_item'] ID: lst_002
[4] suggest_outfit
      in:  new_item ID: lst_002; wardrobe items: 10
      out: Here are two ways to style your new Y2K baby tee using pieces from your wardrobe:  **Outfit 1: 2000s Streetwea…
      →    Used the selected item and saved wardrobe.
```

**Criterion 4 — Try 1**

Query: `black mesh top under $20`

Produced by `tools.py::create_fit_card`, called from `agent.py::run_agent`; selected-item details printed by `run_eval.py::write_report`.

```text
- selected_item: Mesh Long-Sleeve Top — Black ($15.0, depop)

Fit card:
A classic Mesh Long-Sleeve Top in black listed on depop for $15.0 brings instant 90s grunge and Y2K energy to any wardrobe. Layering the sheer black fabric over a white ribbed tank and pairing it with baggy dark denim creates an effortless contrast. Finished with chunky combat boots, the look leans entirely into a dark, textured streetwear aesthetic.
```

**Criterion 5 — Try 1**

Query: `black mesh top under $20`

Produced by `agent.py::run_agent`; search results returned by `mcp_server.py::search_listings`, which calls `tools.py::search_listings`.

```text
[1] parse_query
      in:  black mesh top under $20
      out: {'description': 'black mesh top', 'size': None, 'max_price': 20.0}
[2] search_listings (via MCP)
      in:  {'description': 'black mesh top', 'size': None, 'max_price': 20.0}
      out: 3 items: Mesh Long-Sleeve Top — Black, Biker Shorts — Black, Shiny, Low-Top Canvas Sneakers — Off-White
      →    Matches found: select the first result. Returned IDs and prices: [('lst_017', 15.0), ('lst_026', 14.0), ('lst_035', 20.0)]
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools and returns a fit card | 4 of 5 | MET (5/5) | All five traces show MCP search, suggest_outfit, and create_fit_card completing, with a non-empty caption and no early stop. Five passes meet the original four-pass target. |
| 2 | Impossible query stops before suggest_outfit with a helpful message | 5 of 5 | MET (5/5) | Every try returned an empty search and stopped after the search step. No outfit or fit-card tool ran, and every message named description, size, or maximum price as things to change. |
| 3 | Selected-item ID matches the item passed to suggest_outfit | 5 of 5 | MET (5/5) | In all five tries, the trace records lst_002 in session["selected_item"] and lst_002 as the actual suggest_outfit input. |
| 4 | Fit card includes price and platform and has 2–4 sentences | 4 of 5 | MET (5/5) | All five captions mention the selected item's $15.0 price and depop platform. Their sentence counts are 3, 2, 3, 2, and 3, so all five meet every part of the original criterion. |
| 5 | Every search result respects the maximum price | 5 of 5 | MET (5/5) | Each try parsed a $20.0 maximum and returned prices of $15.0, $14.0, and $20.0. Every returned item was at or below the inclusive ceiling. |

**Diagnoses**

All five criteria were met in `results/run_2026-10-12_0102_before.md`, using the unchanged Unit 3 targets, so there are no failed-criterion diagnoses.

The 5-of-5 targets cover behavior I expected to be deterministic, while the 4-of-5 targets allow some variability from keyword matching or model-generated output. Repeating one known query per criterion limits coverage, and criterion 4's price, platform, and sentence-count checks leave some caption-quality issues untested.

One real weakness appears in criterion 4, Try 2. The caption from `tools.py::create_fit_card` begins:

```text
Scored this Mesh Long-Sleeve Top — Black for just $15.0 on depop, and it is the ultimate piece for building textured looks.
```

The model implied a purchase despite the prompt forbidding that claim, and the tool returned it without validation. The loop and session passed the correct item. This try still passes criterion 4: it includes the price and platform and has two sentences, while unsupported ownership claims are outside that criterion.

I would strengthen criterion 4 in future to also reject unsupported purchase or personal-experience claims. This diagnosis supports the Milestone 5 prompt change below. The original criterion remains unchanged, and the before report preserves the original prompt's results.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```text
$ python app.py ask 'vintage graphic tee under $30' --trace

[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    Matches found: select the first result. Returned IDs and prices: [('lst_002', 18.0), ('lst_006', 24.0), ('lst_033', 19.0), ('lst_015', 26.0), ('lst_017', 15.0), ('lst_003', 22.0), ('lst_011', 27.0), ('lst_012', 20.0), ('lst_013', 30.0), ('lst_014', 12.0)]
[3] select_item
      in:  First search result
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    session['selected_item'] ID: lst_002
[4] suggest_outfit
      in:  new_item ID: lst_002; wardrobe items: 10
      out: Here are two outfit ideas using your new Y2K butterfly baby tee and pieces from your wardrobe:  **Outfit 1: Ca…
      →    Used the selected item and saved wardrobe.
[5] create_fit_card
      in:  new_item ID: lst_002; outfit: Here are two outfit ideas using your new Y2K butterfly baby tee and pieces from …
      out: The Y2K Baby Tee — Butterfly Print listed on depop for $18.0 channels a nostalgic 2000s streetwear vibe. It pa…
      →    All three tools completed.
```

**Empty search**

```text
$ python app.py ask 'designer ballgown size XXS under $5'

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    No matches: stop before suggest_outfit and create_fit_card.

I couldn't find any matching listings. Try changing the description, size, or maximum price.
```

**Empty wardrobe**

```text
$ python app.py ask 'vintage graphic tee under $30' --empty-wardrobe

(running with an empty wardrobe)
[1] parse_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
      →    Matches found: select the first result. Returned IDs and prices: [('lst_002', 18.0), ('lst_006', 24.0), ('lst_033', 19.0), ('lst_015', 26.0), ('lst_017', 15.0), ('lst_003', 22.0), ('lst_011', 27.0), ('lst_012', 20.0), ('lst_013', 30.0), ('lst_014', 12.0)]
[3] select_item
      in:  First search result
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    session['selected_item'] ID: lst_002
[4] suggest_outfit
      in:  new_item ID: lst_002; wardrobe items: 0
      out: Here are two simple ways to style your Y2K baby tee:  *   **Casual Y2K Streetwear:** Pair the tee with mid-ris…
      →    Empty wardrobe: returned general styling advice.
[5] create_fit_card
      in:  new_item ID: lst_002; outfit: Here are two simple ways to style your Y2K baby tee:  *   **Casual Y2K Streetwea…
      out: Channeling total Y2K nostalgia with this Y2K Baby Tee — Butterfly Print, listed on depop for $18.0. The look l…
      →    All three tools completed.

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two simple ways to style your Y2K baby tee:

*   **Casual Y2K Streetwear:** Pair the tee with mid-rise or low-rise blue denim jeans and white chunky sneakers. Add a small shoulder bag and simple silver hoop earrings to complete the look.
*   **Sweet Cottagecore Mix:** Tuck the tee into a pink or lavender tiered midi skirt and wear it with canvas sneakers or strappy flat sandals. Layer a delicate beaded necklace for a soft, feminine touch.

  Fit card: Channeling total Y2K nostalgia with this Y2K Baby Tee — Butterfly Print, listed on depop for $18.0. The look leans into a playful mix of streetwear edge and sweet cottagecore charm depending on the styling. It pairs effortlessly with low-rise denim or a tiered midi skirt for an easy, nostalgic aesthetic.
```

**Model unavailable**

```text
$ python app.py ask 'black mesh top test123 under $20' --trace
[1] parse_query
      in:  black mesh top test123 under $20
      out: {'description': 'black mesh top test123', 'size': None, 'max_price': 20.0}
[2] search_listings (via MCP)
      in:  {'description': 'black mesh top test123', 'size': None, 'max_price': 20.0}
      out: 3 items: Mesh Long-Sleeve Top — Black, Biker Shorts — Black, Shiny, Low-Top Canvas Sneakers — Off-White
      →    Matches found: select the first result. Returned IDs and prices: [('lst_017', 15.0), ('lst_026', 14.0), ('lst_035', 20.0)]
[3] select_item
      in:  First search result
      out: Mesh Long-Sleeve Top — Black ($15.0, depop)
      →    session['selected_item'] ID: lst_017
[4] suggest_outfit
      in:  new_item ID: lst_017; wardrobe items: 10
      out: I couldn't reach the model to suggest an outfit. Check GEMINI_API_KEY in .env and your internet connection, th…
      →    Model unavailable: stop.

I couldn't reach the model to suggest an outfit. Check GEMINI_API_KEY in .env and your internet connection, then try again.

1 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

`search_listings` used to be called directly from `agent.py`. It is now called through `mcp_client.py`, which connects to the registered tool in `mcp_server.py`. The return value stayed a list of listing dictionaries, or `[]` when nothing matched. The rest of the planning loop and the empty-search branch behaved the same: matching results continued to outfit and fit-card generation, while an empty search stopped before both tools.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

I tightened only the `create_fit_card` prompt in `tools.py`. It now explains that the item is a listing under consideration, explicitly rejects implied acquisition phrases such as "Scored this" and "Snagged this," gives a factual alternative using the item's title, price, and platform, and asks the model to check for unsupported claims before returning the caption. The agent, scenarios, original criteria, model, and temperature are unchanged.

**Which failure it was meant to fix:**

Criterion 4, Try 2 in the before report began "Scored this Mesh Long-Sleeve Top — Black," implying an acquisition that the inputs never confirmed. That caption passed the original price/platform/length criterion, so this improvement addresses an observed quality problem rather than a missed target. I scored the same five criteria again and separately compared unsupported acquisition or personal-experience claims in criterion 4's five captions.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before suggest_outfit with a helpful message | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected-item ID matches the item passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes price and platform and has 2–4 sentences | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Every search result respects the maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

After report: [run_2026-10-12_0217_after.md](results/run_2026-10-12_0217_after.md), produced by `run_eval.py::main` / `write_report`. Each scenario ran five times with caching off, using the same queries, wardrobes, model, temperature, and original targets. The full rerun made 50 real model calls. The empty-wardrobe diagnostic also completed successfully in all five tries.

Criterion 4's after-caption sentence counts were 2, 2, 3, 2, and 3; each included $15.0 and depop.

**Real after output — criterion 4, Try 2**

Query: `black mesh top under $20`. Caption returned by `tools.py::create_fit_card`, called from `agent.py::run_agent`:

```text
The Mesh Long-Sleeve Top — Black is listed on depop for $15.0. Layering this piece creates a 90s grunge-streetwear vibe when paired with baggy jeans and combat boots, or a monochrome casual-cool look with wide-leg trousers and a zip hoodie.
```

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

| Measure | Before | After |
|---|---|---|
| Each of the five original criteria | MET (5/5) | MET (5/5) |
| Criterion 4 captions with unsupported acquisition or personal-experience claims (additional diagnostic) | 1 of 5 | 0 of 5 |

The change helped with the diagnosed wording problem in this sample: the before caption implied a purchase with "Scored this," while all five after captions described the listing and styling without unsupported personal claims. Original criterion scores stayed at 5/5, so the measured improvement is in caption quality rather than the acceptance-test pass rate. Five captions are a small sample, and model output varies; this result does not guarantee the problem cannot recur.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

None of the five original criteria are still missed: all five were MET (5/5) in the after evaluation. Each criterion uses one scenario repeated five times, so the results provide limited coverage of other queries and items. Model output can still vary, and the ownership-language improvement from 1/5 to 0/5 was measured on only five captions; it does not guarantee that unsupported claims cannot recur.

I stopped after the required one improvement and full rerun. Next, I would test a wider range of queries and items and collect more uncached captions to check whether the improvement holds beyond this small sample.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
