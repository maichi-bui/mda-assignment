# searcher.py
from whoosh.index import open_dir
from whoosh.query import Or, FuzzyTerm, Prefix, Wildcard

def search_projects(search_term):
    # 1) 打开已有的索引
    ix = open_dir("indexdir")

    # 2) 去掉末尾特殊符号 ~ 或 *
    term = search_term.rstrip("~*")

    # 3) 定义要搜索的字段
    fields = ["title", "acronym", "objective"]

    # ─── 4) 构造复合查询 ─────────────────────────────────────────────
    #    • FuzzyTerm：容忍编辑距离 2，前缀至少 1 字母
    fuzzy_parts  = [FuzzyTerm(f, term, maxdist=2, prefixlength=1) for f in fields]
    #    • Prefix：前缀通配符（term*）
    prefix_parts = [Prefix(f, term)                           for f in fields]
    #    • Wildcard：任意位置通配符，放在前缀之后（*term*）
    wildcard_parts= [Wildcard(f, f"*{term}*")                  for f in fields]

    #    把三种策略统一成一个 Or 查询
    user_query = Or(fuzzy_parts + prefix_parts + wildcard_parts)
    print("DEBUG ▶ user_query =", user_query)
    # ────────────────────────────────────────────────────────────────

    # 5) 执行查询，返回前 20 条
    with ix.searcher() as searcher:
        hits = searcher.search(user_query)

        # 去重处理，使用 projectID 作为唯一标识
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