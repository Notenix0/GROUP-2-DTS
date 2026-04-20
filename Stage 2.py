import csv
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ── Step 1: Load CSV as list of dictionaries ─────────────────
# This is the Christian Hur pattern — CSV → list of dicts
verses = []
with open("proverbs.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        verses.append(row)

print(f"Loaded {len(verses)} verses from CSV\n")

# ── Step 2: Set up tools ──────────────────────────────────────
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# ── Step 3: Preprocessing function ───────────────────────────
def preprocess(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^a-z\s]', '', text)
    # Tokenize (split into individual words)
    tokens = text.split()
    # Remove stopwords and stem each word
    cleaned = []
    for word in tokens:
        if word not in stop_words:
            cleaned.append(stemmer.stem(word))
    return cleaned

# ── Step 4: Apply preprocessing to every verse ───────────────
for verse in verses:
    verse['tokens'] = preprocess(verse['text'])


# ── Step 5: Print preview ─────────────────────────────────────
print("=== PREPROCESSING PREVIEW ===\n")
for verse in verses[:5]:
    print(f"Ch{verse['chapter']} v{verse['verse']}")
    print(f"  Original : {verse['text']}")
    print(f"  Processed: {verse['tokens']}")
    print()