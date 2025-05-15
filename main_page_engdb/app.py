import streamlit as st
import introduction
import dashboard
import search_engine

# 只能调用一次，且必须放在最上方
st.set_page_config(page_title="HORIZON EXPLORER", layout="wide")

# 侧边栏导航
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", [
    "🏠 Introduction",
    "📊 Dashboard", 
    "🔍 Search Engine"
])

# 路由跳转（调用各子页面的 app() 函数）
if page == "🏠 Introduction":
    introduction.app()
elif page == "📊 Dashboard":
    dashboard.app()
elif page == "🔍 Search Engine":
    search_engine.app()
