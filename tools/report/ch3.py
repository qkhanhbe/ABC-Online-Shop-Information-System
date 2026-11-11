import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "diagrams")
R = os.path.join(ROOT, "demo_results")


def section(path, start, end=None):
    text = open(path, encoding="utf-8").read()
    a = text.index(start)
    b = text.index(end, a + 1) if end else len(text)
    return text[a:b].rstrip()


SEARCH_RUN = "$ python main.py demo   (section 1)\n" + section(os.path.join(R, "demo_output.txt"), "  input (text): 'black shoes'", "--- 2.")
EVAL_SEARCH = "$ python evaluate.py\n" + section(os.path.join(R, "evaluation_output.txt"), "=== 1.", "=== 2.")
EVAL_REST = "$ python evaluate.py   (continued)\n" + section(os.path.join(R, "evaluation_output.txt"), "=== 2.")

BLOCKS = [
    ("h1", "CHAPTER 3. AI IN E-COMMERCE"),
    ("p", "Artificial intelligence is useful to ABC Online Shop only where it improves a business activity that the "
          "earlier chapters already described. This chapter therefore does not start from techniques. It starts from "
          "the problems and use cases of Chapters 1 and 2, selects three places where AI helps, analyses each one as a "
          "requirement with data, components, risks and a fallback, and measures the result on test sets."),
    ("h2", "3.1. AI as an Enhancement Layer"),
    ("p", "In the lecture material on integrating AI in the analysis phase, AI is placed as an enhancement layer on top "
          "of the information system, not as a replacement for it. The shop still needs a correct catalogue, correct "
          "stock and correct orders; a search model that ranks perfectly but shows yesterday's stock would make BP02 "
          "worse. The consequence for this essay is a simple rule: every AI component reads the shop's own operational "
          "records through the same DAOs as the rest of the system, and every AI result has a non-AI fallback."),
    ("h2", "3.2. Opportunity Analysis"),
    ("table", "AI opportunities derived from the business problems", ["Activity / problem", "AI opportunity", "Decision"], [
        ["Finding products (UC05, SN01)", "Search by voice and by photo; tolerate synonyms", "Build: multimodal search (from A6)"],
        ["Judging a product (UC06, BP01)", "Summarise many reviews by aspect with evidence", "Build: review insights"],
        ["Moderating reviews (UC18)", "Flag spam and empty reviews for a person", "Build: noise filter, human decides"],
        ["Discovering products (UC06, UC10)", "Recommend similar or complementary products", "Build: content + co-purchase recommender"],
        ["Answering status questions (BP04)", "Natural-language order questions", "Build, restricted to own orders"],
        ["Pricing, fraud scoring", "Dynamic prices, payment risk models", "Not now: no data, provider handles fraud"],
        ["Demand forecasting (SN09)", "Forecast replenishment quantities", "Later: needs months of clean inventory events"]], [45, 65, 55]),
    ("p", "The last two rows matter as much as the first five. AI is not used where the shop lacks the data (demand "
          "forecasting needs a history of reliable inventory events, which the system is only now starting to record) "
          "or where an external party already carries the responsibility (fraud decisions belong to the payment "
          "provider, Section 1.8). An AI feature built on data that does not exist would only add a new way to be wrong."),
    ("h2", "3.3. AI Use Cases"),
    ("p", "The AI functions are modelled as extensions of the Release 1 use cases. The four ways of searching are "
          "specialisations of UC05 Search Products: they share the goal and the flow <i>retrieve, rank, display</i> and "
          "differ only in how the input is read. UC33 View Review Insights and UC34 View Recommendations extend UC06 View "
          "Product Details, because a product page must remain usable without them. A speech/vision engine appears as a "
          "secondary actor so that the boundary of the AI service is visible."),
    ("fig", os.path.join(D, "UC_AI AI-Enabled Use Cases.png"), "AI-enabled use cases - VP diagram \"UC_AI AI-Enabled Use Cases\"", 160),
    ("h2", "3.4. Multimodal Search: Principles"),
    ("p", "The search service of Assignment 06 is built on one principle: different inputs are converted into one common "
          "query representation, and from there the processing is the same."),
    ("eq", "text q<sub>t</sub> → z<sub>t</sub>,&nbsp;&nbsp; voice q<sub>v</sub> → text → z<sub>t</sub>,&nbsp;&nbsp; image q<sub>i</sub> → z<sub>i</sub>,&nbsp;&nbsp; then retrieval → ranking → results"),
    ("p", "<b>Query understanding.</b> QueryService normalises the text, removes stop words, extracts a price filter "
          "(\"under 100 dollars\" → max_price = 100) and maps synonyms (\"sneakers\" → shoes, \"handbag\" → bag). "
          "The synonym table is new in this essay; it addresses the main error class reported in Assignment 06. A "
          "sentence that contains the word <i>order</i> becomes an order query that always carries the customer id of "
          "the session (AI-R2)."),
    ("p", "<b>Voice.</b> SpeechService.transcribe(audio) returns text. In the prototype the speech recognition is "
          "<b>simulated</b>: the argument already is the sentence that a speech-to-text engine would return. The method "
          "is the seam where a real engine such as Whisper is plugged in without changing any caller (AI-N1)."),
    ("p", "<b>Images.</b> ImageService.encode(image) is a hand-made encoder f(I) → z of 128 values: a 4×4×4 RGB "
          "histogram of the object's pixels (colour) and an 8×8 occupancy grid of the object mask (shape), both "
          "L2-normalised. The background colour is estimated from the image border, so a photo on a different background "
          "still matches. Retrieval uses cosine similarity and keeps the top k:"),
    ("eq", "s(I<sub>q</sub>, I<sub>p</sub>) = z<sub>q</sub><sup>T</sup>z<sub>p</sub> / (||z<sub>q</sub>|| ||z<sub>p</sub>||),&nbsp;&nbsp;&nbsp; R(q) = TopK<sub>x∈X</sub> s(q, x)"),
    ("h2", "3.5. Retrieval and Ranking"),
    ("p", "Retrieval and ranking are separate steps and separate classes. SearchService.retrieve builds the candidate set "
          "C(q) from keyword matches and from the image index; RankingService.rank orders it. The separation lets the "
          "business change its ranking policy without touching retrieval. The final score combines three signals:"),
    ("eq", "S(x|q) = α·S<sub>text</sub> + β·S<sub>image</sub> + γ·S<sub>business</sub>"),
    ("bullets", [
        "S<sub>text</sub> = matched query words / number of query words; S<sub>image</sub> = cosine similarity (0..1);",
        "S<sub>business</sub> = 0.8·[available &gt; 0] + 0.2·min(available, 20)/20, read from the shop's own stock (stock-aware ranking);",
        "text and voice: (α, β, γ) = (0.9, 0, 0.1); image: (0, 0.9, 0.1); text + image: α = 0.9·λ<sub>t</sub>, β = 0.9·λ<sub>i</sub>, λ<sub>t</sub> + λ<sub>i</sub> = 1 (default 0.5/0.5)."]),
    ("p", "The architecture keeps the three layers of Assignment 06, now inside the shop: the presentation layer is the "
          "shop's controller and view, the application-intelligence layer contains the five AI services, and the data "
          "layer contains the same ProductDAO, InventoryDAO and OrderDAO that the checkout uses, plus VectorIndex and "
          "ImageStorage. Every dependency points downwards."),
    ("fig", os.path.join(D, "CMP01 AI Search Three-Layer Architecture.png"), "Three-layer architecture of the search subsystem - VP diagram \"CMP01 AI Search Three-Layer Architecture\"", 165),
    ("p", "One dependency needed care. VectorIndex must call the encoder to index the product images, but the encoder "
          "lives in the layer above. Instead of letting the data layer import upwards, the composition root passes the "
          "encoding function in: VectorIndex.build(storage, products, encode). The two sequence diagrams below show "
          "voice and image search with the real method names of the code."),
    ("fig", os.path.join(D, "SD03 Voice Search.png"), "Voice search - VP diagram \"SD03 Voice Search\"", 160),
    ("fig", os.path.join(D, "SD04 Image Search.png"), "Image search - VP diagram \"SD04 Image Search\"", 160),
    ("p", "Running the four query types on the seeded shop gives the trace below. Each line names the component that "
          "performs the step, so a run can be followed on the sequence diagrams. The voice query shows the stock-aware "
          "ranking: Nike Court Sneakers matches both words and is the only Nike shoe under 100 dollars, but it is out "
          "of stock, so its business score is 0 and its final score 0.900 instead of 0.990. The text + image query shows "
          "why combining modalities helps: three products match both words, and only the photo can tell that the "
          "customer wants the red pair."),
    ("term", SEARCH_RUN, "Output of the search part of main.py demo: text, voice, image, text + image", 150),
    ("h2", "3.6. Review Insights"),
    ("p", "Assignment 02 proposed a PhoBERT aspect-based sentiment model to turn reviews into evidence for customers and "
          "managers. The prototype keeps the same interface, analyse(reviews) → per-aspect sentiment with evidence, "
          "but implements it with a transparent lexicon so that it runs offline and every label can be explained. The "
          "pipeline is drawn as an activity diagram; the decision nodes are the two places where the component falls "
          "back instead of guessing."),
    ("fig", os.path.join(D, "AD04 Review Insight Pipeline.png"), "Review insight pipeline - VP diagram \"AD04 Review Insight Pipeline\"", 100),
    ("bullets", [
        "<b>Noise filter.</b> Links, long digit strings (phone numbers), repeated characters and texts with fewer than two words are noise. Noise is skipped in the statistics and, when a customer submits it, the review waits for moderation (AI-R5).",
        "<b>Clauses.</b> A review is split at sentence punctuation, commas and the words <i>but</i>/<i>however</i>, because one review often praises one aspect and criticises another.",
        "<b>Aspects and polarity.</b> Each clause is matched against four aspect vocabularies (quality, price, delivery, service; English and a few Vietnamese words). Polarity is the sum of positive and negative words, with a negation in the three previous words flipping a word (\"not fast\" is negative).",
        "<b>Aggregation.</b> Positive and negative counts per aspect, the positive share, two evidence sentences, and a label: Mostly positive (share ≥ 0.7), Mixed (≥ 0.4) or Mostly negative. With fewer than two usable reviews the label is \"Not enough reviews\" (AI-N3)."]),
    ("h2", "3.7. Recommendation"),
    ("p", "The recommender combines two signals computed from the shop's records. Content similarity is the cosine of "
          "TF-IDF vectors built from name, category, brand, colour and description; it works for a new product that "
          "nobody has bought yet. Co-purchase counts how often two products were in the same non-cancelled order; it "
          "captures complements that text cannot (a cap bought with running shoes)."),
    ("eq", "score(p, q) = 0.7·cos(tfidf<sub>p</sub>, tfidf<sub>q</sub>) + 0.3·copurchase(p, q) / max<sub>r</sub> copurchase(p, r)"),
    ("p", "Out-of-stock products are never recommended, and a customer is never recommended something already bought "
          "(cancelled and failed orders do not count as purchases). These are business rules, not model parameters; "
          "they are enforced in RecommenderService and checked by a test."),
    ("h2", "3.8. Data Requirements"),
    ("table", "Data cards of the AI components", ["Component", "Input data and source", "Quality and constraints"], [
        ["Multimodal search", "16 products (name, category, brand, colour, price) from ProductDAO; stock from InventoryDAO; "
                              "16 catalogue images and 10 query photos (synthetic drawings)",
         "Images are drawings, so accuracy does not transfer to real photos; stock is read live"],
        ["Speech", "Transcript standing for audio (simulation)", "No audio stored; a real engine must not keep recordings"],
        ["Review insights", "Published reviews from ReviewDAO (14 seeded); 30 hand-labelled reviews with 39 aspect labels for evaluation",
         "Only reviews linked to a delivered order; no personal data used"],
        ["Recommender", "Product text; 16 seeded orders (co-purchase)", "Cold start handled by content similarity"],
        ["Order questions", "Orders of the session customer only (OrderDAO.find_by_customer)", "Never reads another customer's orders (NFR05)"]], [32, 75, 58]),
    ("h2", "3.9. Evaluation"),
    ("p", "The search was evaluated on 26 queries: the 20 queries of Assignment 06 and six new ones that test the synonym "
          "table, the four new products and the privacy rule (query 26 asks for another customer's order and is "
          "successful only if nothing is returned). A query is successful when the top-1 result is the expected product "
          "or order."),
    ("term", EVAL_SEARCH, "Output of evaluate.py, part 1: multimodal search on 26 test queries", 165),
    ("p", "The success rate is 24/26 = 92.3% (text 6/7, voice 4/4, image 9/9, multimodal 2/3, order 3/3). The review "
          "analyser and the recommender were evaluated on their own test data:"),
    ("term", EVAL_REST, "Output of evaluate.py, parts 2 and 3: review insights and recommender", 150),
    ("table", "Evaluation summary", ["Component", "Metric", "Value"], [
        ["Search", "Top-1 success rate", "24 / 26 = 92.3%"],
        ["Search", "Image queries / order queries (incl. privacy)", "9 / 9, 3 / 3"],
        ["Review insights", "Aspect detection precision / recall / F1", "0.97 / 0.95 / 0.96"],
        ["Review insights", "Polarity accuracy on detected aspects", "35 / 37 = 0.95"],
        ["Recommender", "Same-category hit rate of top-3", "28 / 48 = 0.58"],
        ["Recommender", "Coverage / out-of-stock recommended", "15 / 15 / 0"]], [40, 80, 45]),
    ("h2", "3.10. Error Analysis"),
    ("bullets", [
        "<b>Query 18 \"nike\" + white shoe photo.</b> The expected Nike Court Sneakers has the more similar image but is out of stock, so it loses 0.09 business points and Nike Running Shoes wins (0.801). This is the same trade-off as in Assignment 06; it shows that γ must be tuned on real behaviour.",
        "<b>Query 21 \"white sneakers\".</b> The synonym table maps <i>sneakers</i> to <i>shoes</i>, so the word that identified the court sneakers is lost and Adidas Running Shoes (white, in stock) wins. Mapping to both words, or embedding-based text matching, would keep the specific term. A fix for one error class created another, which is why the test set is run on every change.",
        "<b>Review insights.</b> The five errors are typical lexicon limits: an aspect word used as a reference (\"too expensive for this quality\"), an opinion split from its aspect by a comma (\"shipping took two weeks, very slow\"), two aspects with opposite polarity in one clause, and missing Vietnamese vocabulary. Sarcasm (\"Oh great, another two weeks\") was classified correctly only because the star rating broke the tie.",
        "<b>Recommender.</b> A hit rate of 0.58 is low only if the goal is \"more of the same\". Many top-3 lists mix a same-category item with a complement bought together (shoes and caps), which is intended by the 0.3 co-purchase weight."]),
    ("h2", "3.11. Risks, Fallbacks and Human Control"),
    ("table", "AI risks and the design response", ["Risk", "Effect", "Response (fallback / control)"], [
        ["Wrong top result", "Customer misses the product", "Show top-5 with scores; keyword search and category browsing always available"],
        ["Speech or image engine unavailable", "Voice/photo search fails", "Text search unchanged; error message instead of empty page"],
        ["Ranking hides out-of-stock items", "Customer cannot find a known product", "Out-of-stock items are ranked lower, never removed from text results"],
        ["Spam or abusive review", "Misleading product page", "Noise is held for moderation; an Administrator publishes or rejects (UC18)"],
        ["Misleading review summary", "Wrong purchase decision", "Evidence sentences shown next to the counts; full review list below"],
        ["Order question leaks data", "Privacy breach", "Order queries carry the session customer id; tested with another customer's order"],
        ["Feedback loop in recommendations", "Popular items get more popular", "Content similarity keeps new items visible; coverage measured"]], [42, 45, 78]),
    ("p", "Human control is designed in at two points. Reviews flagged as noise are never published automatically; they "
          "appear in the moderation queue, where a person decides. And no AI component can change an order, a price or "
          "a stock level: AI only ranks, labels and suggests. Every state change still goes through the services and "
          "rules of Chapter 4."),
    ("h2", "3.12. Technology Options for a Production Version"),
    ("table", "Prototype components and production replacements", ["Prototype", "Production option", "What stays the same"], [
        ["SpeechService (simulated)", "Whisper or a cloud speech API with Vietnamese support", "transcribe(audio) -> text"],
        ["ImageService (colour + shape)", "CLIP image encoder (shared space with text)", "encode(image) -> vector"],
        ["VectorIndex (in memory)", "FAISS or a vector database", "search(z, k) -> [(id, score)]"],
        ["Lexicon review analyser", "PhoBERT fine-tuned for ABSA (Assignment 02)", "analyse(reviews) -> aspects, label"],
        ["TF-IDF + co-purchase", "Matrix factorisation / two-tower model with click data", "similar(id, k), for_customer(id, k)"]], [45, 70, 50]),
    ("p", "The right-hand column is the important one: the interfaces were fixed in Chapter 1 as AI-N1, so each replacement "
          "is a change in one class plus the composition root, and the 40 tests of Chapter 5 continue to describe the "
          "behaviour that the shop expects."),
    ("h2", "3.13. Chapter Summary"),
    ("p", "Three AI components were analysed like any other requirement: they come from business problems, extend "
          "existing use cases, read the shop's own data, have fallbacks and are measured. The search keeps the "
          "Assignment 06 design and reaches 92.3% top-1 success on 26 queries; the review analyser reaches an aspect F1 "
          "of 0.96; the recommender never suggests unavailable or already-bought items. The honest limits (synthetic "
          "images, simulated speech, a lexicon instead of a trained model) are stated together with the production "
          "replacements that the interfaces allow."),
]
