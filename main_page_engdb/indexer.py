import os
import pandas as pd
from tqdm import tqdm
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer

# 📂 定义索引文件夹
index_dir = "indexdir"

# 📝 定义搜索 schema，仅保留关键字段
schema = Schema(
    id=ID(stored=True),
    acronym=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    objective=TEXT(stored=True, analyzer=StemmingAnalyzer())
)

# 🔄 创建索引目录
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

ix = create_in(index_dir, schema)

# 📊 读取 CSV 文件
df = pd.read_csv("horizon-dataset/cleaned-data/projects.csv", dtype=str, encoding="utf-8-sig")[["id", "acronym", "title", "objective"]].drop_duplicates()
df.rename(columns={"id": "projectID"}, inplace=True)

# ⚠️ 填充缺失值，避免报错
df.fillna("", inplace=True)

# ✏️ 添加文档
writer = ix.writer()
for row in tqdm(df.to_dict(orient="records")):
    writer.add_document(
        projectID=row["projectID"],
        acronym=row["acronym"],
        title=row["title"],
        objective=row["objective"]
    )

writer.commit()
print("Indexing completed.")
