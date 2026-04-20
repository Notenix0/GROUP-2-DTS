import csv
import re

# ── Read raw file ──────────────────────────────────────────────
with open("proverbs_raw.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# ── Known section headings to skip ────────────────────────────
headings = {"The Enticement of Sinners", "Wisdom Warns"}

verses = []
chapter = 1
current_verse_num = None
current_text = []

def save_verse():
    """Save the current verse buffer into the verses list."""
    if current_verse_num is not None and current_text:
        full_text = " ".join(current_text).strip()
        verses.append({
            "chapter": chapter,
            "verse": current_verse_num,
            "text": full_text
        })

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Remove footnote markers e.g [a], [b], [j]
    line = re.sub(r'\[[a-z]\]', '', line).strip()

    # Skip section headings
    if line in headings:
        continue

    # Check if line starts with a verse number
    match = re.match(r'^(\d+)\s+(.*)', line)

    if match:
        verse_num = int(match.group(1))
        verse_text = match.group(2)

        # ── Detect chapter switch ──────────────────────────────
        # If verse number drops back to 2 after 33, we're in Chapter 2
        # The unnumbered text before "2 Make your ear..." is Chapter 2 verse 1
        if chapter == 1 and verse_num == 2 and current_verse_num == 33:
            # Save verse 33 of chapter 1
            save_verse()
            # The buffered continuation lines after 33 = Chapter 2 verse 1
            chapter = 2
            current_verse_num = 1
            current_text = []  # already saved in save_verse above


        elif chapter == 1 and current_verse_num is not None and verse_num < current_verse_num:
            # Generic fallback for chapter switch
            save_verse()
            chapter = 2
            current_verse_num = 1
            current_text = []

        else:
            # Normal new verse — save previous first
            save_verse()
            current_verse_num = verse_num
            current_text = [verse_text]
            continue

        current_verse_num = verse_num
        current_text = [verse_text]

    else:
        # ── Continuation line ──────────────────────────────────
        # Special case: unnumbered Chapter 2 verse 1
        if current_verse_num == 33 and chapter == 1:
            # This text belongs to Chapter 2 verse 1, not verse 33
            save_verse()
            chapter = 2
            current_verse_num = 1
            current_text = [line]
        else:
            if current_text is not None:
                current_text.append(line)

# Save the very last verse
save_verse()

# ── Write CSV ──────────────────────────────────────────────────
with open("proverbs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["chapter", "verse", "text"])
    writer.writeheader()
    writer.writerows(verses)

print(f"Done! {len(verses)} verses written to proverbs.csv")

# ── Quick check ────────────────────────────────────────────────
for v in verses:
    print(f"Ch{v['chapter']} v{v['verse']}: {v['text']}")