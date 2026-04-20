import csv
import re
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))


# ── Step 1: Load CSV (Christian Hur pattern) ───────────────────
verses = []
with open("proverbs.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        verses.append(row)

# ── Step 2: Preprocess ─────────────────────────────────────────
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    return [stemmer.stem(w) for w in tokens if w not in stop_words]

for verse in verses:
    verse['tokens'] = preprocess(verse['text'])

# ── Step 3: TF (Term Frequency) ────────────────────────────────
# How often does the query word appear in THIS verse?
def compute_tf(tokens, term):
    if len(tokens) == 0:
        return 0
    return tokens.count(term) / len(tokens)

# ── Step 4: IDF (Inverse Document Frequency) ───────────────────
# How rare is the query word across ALL verses?
def compute_idf(verses, term):
    # Count how many verses contain the term
    containing = sum(1 for v in verses if term in v['tokens'])
    if containing == 0:
        return 0
    return math.log(len(verses) / containing)

# ── Step 5: TF-IDF Score ───────────────────────────────────────
def compute_tfidf(tf, idf):
    return tf * idf

# ── Step 6: Run query ──────────────────────────────────────────
query = "wisdom"
query_stem = stemmer.stem(query)  # stem the query too

idf = compute_idf(verses, query_stem)

results = []
for verse in verses:
    tf = compute_tf(verse['tokens'], query_stem)
    score = compute_tfidf(tf, idf)
    if score > 0:
        results.append({
            "chapter": verse['chapter'],
            "verse": verse['verse'],
            "text": verse['text'],
            "score": round(score, 4)
        })

# ── Step 7: Rank by score (highest first) ─────────────────────
results.sort(key=lambda x: x['score'], reverse=True)

# ── Step 8: Display ────────────────────────────────────────────
print(f"=== TF-IDF RESULTS FOR: '{query}' ===\n")
print(f"IDF Score for '{query}': {round(idf, 4)}")
print(f"Found in {len(results)} verses — ranked by relevance:\n")

for i, r in enumerate(results, 1):
    print(f"Rank {i} — Proverbs {r['chapter']}:{r['verse']} (Score: {r['score']})")
    print(f"  {r['text']}")
    print()