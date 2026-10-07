"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings
import re

# ── Tool 1: search_listings ───────────────────────────────────────────────────

#Helper function to check if the requested size matches the actual size in the listing
def _size_matches(requested: str, actual: str) -> bool:
    requested = requested.strip().lower()
    actual = actual.strip().lower()

    #Exact match
    if requested == actual:
        return True

    #Letter sizes: S, M, L, XL, etc.
    letter_sizes = {"xxs", "xs", "s", "m", "l", "xl", "xxl", "xxxl"}

    if requested in letter_sizes:
        actual_sizes = re.findall(
            r"(?<![a-z0-9])(xxxl|xxl|xxs|xl|xs|s|m|l)(?![a-z0-9])",
            actual,
        )
        return requested in actual_sizes

    #Waist/inseam style sizes such as W30 or L30
    if re.fullmatch(r"[wl]\d+", requested):
        return re.search(
            rf"(?<![a-z0-9]){re.escape(requested)}(?![a-z0-9])",
            actual,
        ) is not None

    #Numeric sizes such as shoe size 8
    if re.fullmatch(r"\d+(?:\.\d+)?", requested):
        return re.search(
            rf"(?<!\d){re.escape(requested)}(?!\d)",
            actual,
        ) is not None

    return False


#Implemented the search_listings function to filter thrift listings based on description, size, and max price. It loads listings, applies filters, scores them based on keyword overlap, and returns the best matches.
def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
        
    listings = load_listings()

    keywords = set(re.findall(r"[a-z0-9]+", description.lower()))

    scored_results = []

    for listing in listings:

        # Price filter
        if max_price is not None and listing["price"] > max_price:
            continue

        # Size filter
        if size is not None and not _size_matches(size, listing["size"]):
            continue

        # Combine useful searchable fields
        searchable_text = " ".join([
            listing.get("title", ""),
            listing.get("description", ""),
            listing.get("category", ""),
            " ".join(listing.get("style_tags", [])),
            " ".join(listing.get("colors", [])),
            listing.get("brand") or "",
            listing.get("condition", ""),
            listing.get("platform", ""),
        ]).lower()

        searchable_words = set(re.findall(r"[a-z0-9]+", searchable_text))

        # Count how many description keywords appear in the listing
        score = sum(1 for word in keywords if word in searchable_words)

        if score > 0:
            scored_results.append((score, listing))

    # Highest score first
    scored_results.sort(key=lambda pair: pair[0], reverse=True)

    # Return only the listing dictionaries, not their scores
    return [
        listing
        for score, listing in scored_results[:config.SEARCH_RESULT_LIMIT]
    ]

    


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

#Implemented the suggest_outfit function to provide outfit suggestions based on a new thrifted item and the user's existing wardrobe. The function checks if the wardrobe is empty and generates general styling advice if it is. If the wardrobe has items, it formats them into a prompt for the model to suggest specific outfit combinations. 
def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = wardrobe.get("items", [])

    # Basic information about the new thrift item
    item_info = (
        f"Title: {new_item.get('title', 'Unknown item')}\n"
        f"Category: {new_item.get('category', 'unknown')}\n"
        f"Colors: {', '.join(new_item.get('colors', []))}\n"
        f"Style tags: {', '.join(new_item.get('style_tags', []))}\n"
    )

    # Empty wardrobe case
    if not items:
        prompt = f"""
    You are a fashion styling assistant.

    The user is considering this thrifted item:

    {item_info}

    The user does not have any saved wardrobe items yet.

    Suggest one or two simple ways they could style this item using
    general clothing pieces. Keep the response concise and practical.
    """
        return generate(prompt).strip()

    # Format the user's wardrobe
    wardrobe_lines = []

    for item in items:
        wardrobe_lines.append(
            f"- {item.get('name', 'Unnamed item')} "
            f"({item.get('category', 'unknown')}; "
            f"colors: {', '.join(item.get('colors', []))}; "
            f"styles: {', '.join(item.get('style_tags', []))})"
        )

    wardrobe_text = "\n".join(wardrobe_lines)

    prompt = f"""
    You are a fashion styling assistant.

    The user is considering this thrifted item:

    {item_info}

    The user already owns these wardrobe pieces:

    {wardrobe_text}

    Suggest one or two outfits that use the new thrifted item together
    with pieces from the user's wardrobe. Name the wardrobe pieces you
    are using so the suggestion is specific.

    Keep the response concise and practical.
    """

    return generate(prompt).strip()
 


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """

    # Check if we received a valid outfit suggestion
    if not outfit or not outfit.strip():
        return "A fit card could not be created because no outfit suggestion was provided."

    # Get the information we need from the selected item
    title = new_item.get("title", "Unknown item")
    price = new_item.get("price", "Unknown")
    platform = new_item.get("platform", "Unknown")
    style_tags = ", ".join(new_item.get("style_tags", []))

    # Build the prompt for Gemini
    prompt = f"""
    You are writing a short social media caption for a thrifted outfit.

    Here is the thrifted item:
    - Title: {title}
    - Price: ${price}
    - Platform: {platform}
    - Style: {style_tags}

    Here is the outfit suggestion:
    {outfit}

    Write a natural, engaging caption following these rules:

    1. Use 2 to 4 sentences.
    2. Mention the thrifted item by name.
    3. Mention its price (${price}) exactly once.
    4. Mention the platform ({platform}) exactly once.
    5. Describe the overall outfit's style or vibe.
    6. Make it sound like a real social media post, not a product description.
    7. Present the item and outfit as a social-style caption, but do not write from the perspective of a seller, do not use sales language such as "available now," "grab it," or "shop now."
    8. Do not claim the user bought, found, wore, or personally experienced the item. Describe the outfit and listing using only the provided information.
    9. Avoid first-person claims or opinions such as "I love", "I wore", "I bought", or "I found". Keep the caption natural but factual.

    Return only the finished caption.
    """

    return generate(prompt).strip()
