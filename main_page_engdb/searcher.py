# searcher.py
from whoosh.index import open_dir
from whoosh.query import Or, FuzzyTerm, Prefix, Wildcard, Term

def search_projects(search_term):
    # 1) open the index directory
    ix = open_dir("main_page_engdb/indexdir")

    # 2) remove trailing wildcards
    term = search_term.rstrip("~*")

    # 3) define the fields to search
    fields = ["title", "acronym", "objective"]

    # if the search term is a number, we assume it's a projectID
    if search_term.isdigit():
        user_query = Term("projectID", search_term)
    else:
        # ─── 4) build composite searching ─────────────────────────────────────────────
        #    • FuzzyTerm: typo tolerance, 2 characters max distance
        fuzzy_parts  = [FuzzyTerm(f, term, maxdist=2, prefixlength=1) for f in fields]
        #    • Prefix: prefix search, 1 character min length
        prefix_parts = [Prefix(f, term)                           for f in fields]
        #    • Wildcard: wildcard search, 1 character min length
        wildcard_parts= [Wildcard(f, f"*{term}*")                  for f in fields]

        #    combine all parts into a single query
        user_query = Or(fuzzy_parts + prefix_parts + wildcard_parts)

    print("DEBUG ▶ user_query =", user_query)

    # 5) execute the search
    with ix.searcher() as searcher:
        hits = searcher.search(user_query)

        # remove duplicates by projectID
        unique_hits = {hit["projectID"]: hit for hit in hits}.values()

        return [
            {
                "projectID": hit["projectID"],
                "acronym":   hit["acronym"],
                "title":     hit["title"],
                "objective": hit["objective"],
            }
            for hit in unique_hits
        ]