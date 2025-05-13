1.delete indexdir folder (not indexer.py!!!!!)
2.run indexer.py
3.run searcher.py
4.change the path of project_df(line 26) and org_df(line 27) in search_engine.py to your path
5.run pp.py

##
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
venv\Scripts\activate
streamlit cache clear
###
cd "C:\Users\lu\Desktop\KUL semester2\mda\EngineDashboard"
streamlit run pp.py

cd main_page_engdb

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))