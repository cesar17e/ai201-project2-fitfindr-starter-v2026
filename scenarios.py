"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Five numbered scenarios cover the criteria in criteria.md. The empty-wardrobe
scenario is an additional diagnostic run, separate from those five criteria.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Criterion 3: compare session['selected_item']['id'] with the actual
        # new_item ID in the suggest_outfit trace. Both must be the same.
        "name": "selected item stays consistent across tools",
        "query": "vintage graphic tee under $30, size M",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: check the actual caption for the selected item's price
        # and platform, and a length of two to four sentences. The runner
        # repeats this same query five times with caching disabled.
        "name": "fit card includes price and platform in two to four sentences",
        "query": "black mesh top under $20",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5: compare EVERY returned price in the search trace with
        # the parsed $20 ceiling, rather than checking only the selected item.
        # The dataset contains matching items both at and above this ceiling.
        "name": "every search result respects the maximum price",
        "query": "black mesh top under $20",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
