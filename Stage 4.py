import csv
import re
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# ── Load CSV ───────────────────────────────────────────────────
verses = []
with open("proverbs.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        verses.append(row)

# ── Preprocess ─────────────────────────────────────────────────
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    return [stemmer.stem(w) for w in tokens if w not in stop_words]

for verse in verses:
    verse['tokens'] = preprocess(verse['text'])

# ── TF, IDF, TF-IDF ───────────────────────────────────────────
def compute_tf(tokens, term):
    if len(tokens) == 0:
        return 0
    return tokens.count(term) / len(tokens)

def compute_idf(verses, term):
    containing = sum(1 for v in verses if term in v['tokens'])
    if containing == 0:
        return 0
    return math.log(len(verses) / containing)

# ── Frequency Analysis ─────────────────────────────────────────
def frequency_analysis(verses, query):
    ch1 = sum(1 for v in verses if v['chapter'] == '1' and query in v['tokens'])
    ch2 = sum(1 for v in verses if v['chapter'] == '2' and query in v['tokens'])
    total = ch1 + ch2
    print(f"\n=== FREQUENCY ANALYSIS: '{query}' ===")
    print(f"  Proverbs 1 : {ch1} verses")
    print(f"  Proverbs 2 : {ch2} verses")
    print(f"  Total      : {total} verses out of 55\n")

# ── Main Search Function ───────────────────────────────────────
def search(query):
    query_stem = stemmer.stem(query.lower())
    idf = compute_idf(verses, query_stem)

    if idf == 0:
        print(f"\n  '{query}' not found in any verse.\n")
        return

    results = []
    for verse in verses:
        tf = compute_tf(verse['tokens'], query_stem)
        score = tf * idf
        if score > 0:
            results.append({
                "chapter": verse['chapter'],
                "verse":   verse['verse'],
                "text":    verse['text'],
                "score":   round(score, 4)
            })

    results.sort(key=lambda x: x['score'], reverse=True)

    frequency_analysis(verses, query_stem)

    print(f"=== TF-IDF RESULTS FOR: '{query}' ===")
    print(f"  IDF Score : {round(idf, 4)}")
    print(f"  Found in  : {len(results)} verses\n")

    for i, r in enumerate(results, 1):
        print(f"  Rank {i} — Proverbs {r['chapter']}:{r['verse']} (Score: {r['score']})")
        print(f"  {r['text']}")
        print()

# ── Query Interface ────────────────────────────────────────────
print("=" * 50)
print("   BIBLE IR SYSTEM — Proverbs 1 & 2 (NASB 1995)")
print("=" * 50)

while True:
    query = input("\nEnter search word (or 'quit' to exit): ").strip()
    if query.lower() == 'quit':
        print("\nExiting system. Goodbye!")
        break
    elif query == '':
        print("  Please enter a word.")
    else:
        search(query)