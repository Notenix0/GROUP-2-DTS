import csv

# ── Step 1: Load CSV as list of dictionaries (Christian Hur pattern) ──
verses = []
with open("proverbs.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        verses.append(row)

print(f"Loaded {len(verses)} verses\n")

# ── Step 2: Search function (Christian Hur pattern) ────────────────────
def search_verses(verse_list, query):
    results = []
    for verse in verse_list:
        # Check if query substring exists in the verse text
        if query.lower() in verse['text'].lower():
            results.append(verse)
            break  # Christian Hur bug fix — stop after first match per verse
    return results

# ── Step 3: Fix — search ALL verses not just first match ───────────────
def search_all_verses(verse_list, query):
    results = []
    for verse in verse_list:
        if query.lower() in verse['text'].lower():
            results.append(verse)  # collect every matching verse
    return results

# ── Step 4: Run the query ───────────────────────────────────────────────
query = "wisdom"
results = search_all_verses(verses, query)

# ── Step 5: Display results ─────────────────────────────────────────────
print(f"=== SEARCH RESULTS FOR: '{query}' ===\n")
print(f"Found in {len(results)} verses:\n")

for verse in results:
    print(f"Proverbs {verse['chapter']}:{verse['verse']}")
    print(f"  {verse['text']}")
    print()