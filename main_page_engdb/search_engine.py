import streamlit as st
from searcher import search_projects
from create_network import create_project_network
import pandas as pd

if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

def app():
    st.title("Welcome to the Search Engine Page")
    st.write("This is the Search Engine section.")
    
    project_df = pd.read_csv('project_geo.csv', encoding="utf-8-sig")
    org_df = pd.read_csv('organization.csv', encoding="utf-8-sig") 

    if "selected_project_id" not in st.session_state:
        st.session_state.selected_project_id = None
    if "page" not in st.session_state:
        st.session_state.page = "🔍 Search"
    if "latest_results" not in st.session_state:
        st.session_state.latest_results = []

    # Sidebar 显示当前页面状态
    #st.sidebar.title("Navigation")
    #st.sidebar.write(f"Current Page: {st.session_state.page}")

    # 如果在详情页，添加回退按钮
    if st.session_state.page == "📄 Project Detail":
        if st.sidebar.button("🔙 Back to Search"):
            st.session_state.page = "🔍 Search"
            st.session_state.selected_project_id = None

    # 搜索页
    if st.session_state.page == "🔍 Search":
        st.title("🔍 EU Project Search Engine")
        query = st.text_input("Enter keywords to search (projectID, acronym, title, or objective). You can make typos, enter partial words, or use * as a wildcard.")

        if query:
            results = search_projects(query)
            st.session_state.latest_results = results  # 缓存搜索结果
            st.write(f"Found {len(results)} result(s):")

            for index, r in enumerate(results):
                st.markdown(f"**{r['title']}**")
                st.write(f"Project ID: `{r['projectID']}`")
                st.write(f"Acronym: {r['acronym']}")
                truncated_objective = r['objective'][:100] + "..." if len(r['objective']) > 100 else r['objective']
                st.write(f"Objective: {truncated_objective}")

                if st.button(f"View Details: {r['projectID']}", key=f"view_{r['projectID']}_{index}", on_click=click_button):
                    st.session_state.selected_project_id = r['projectID']
                    st.session_state.page = "📄 Project Detail"

    # 详情页
    elif st.session_state.page == "📄 Project Detail":
        st.title("📄 Project Details")

        # 获取选中的项目 ID
        project_id = st.session_state.selected_project_id
        st.subheader(f"Project ID: {project_id}")

        # 确保数据类型一致
        project_df['projectID'] = project_df['projectID'].astype(str)
        project_id = str(project_id)

        # 获取项目详细信息
        filtered_project = project_df[project_df['projectID'] == project_id]
        if filtered_project.empty:
            st.error(f"No project found with Project ID: {project_id}")
            st.stop()  # 停止执行后续代码
        else:
            project = filtered_project.iloc[0]

            # 显示项目基本信息
            st.markdown(f"""
            ### {project['title']} ({project['acronym']})
            **Status:** {project['status']}  
            **Duration:** {project['startDate']} to {project['endDate']}  
            **Total Cost:** €{project['totalCost']}  
            **EU Contribution:** €{project['ecMaxContribution']}  
            **Topics:** {project['topics']}  
            **Funding Scheme:** {project['fundingScheme']}
            **DOI:** [https://doi.org/{project['grantDoi']}](https://doi.org/{project['grantDoi']})
            """)

            # 显示项目目标
            st.markdown("### Project Objective")
            st.write(project['objective'])

            # 显示参与组织信息
            st.markdown("### Participating Organisations")

            # 确保数据类型一致
            org_df['projectID'] = org_df['projectID'].astype(str)
            project_id = str(project_id)

            # 筛选参与组织
            participating_orgs = org_df[org_df['projectID'] == project_id]

            # # 调试信息
            # print(f"Selected Project ID: {project_id}")
            # print(f"Number of matching organizations: {len(participating_orgs)}")
            # print("Sample data in participating_orgs:")
            # print(participating_orgs.head())

            # 显示组织信息表格
            if participating_orgs.empty:
                st.warning("No participating organizations found for this project.")
            else:
                # 重置索引以隐藏默认的数字索引
                participating_orgs_display = participating_orgs[['name', 'country', 'activityType', 'city', 'SME', 'role', 'organizationURL']].reset_index(drop=True)
                st.dataframe(participating_orgs_display, use_container_width=True)
                
            # 生成网络图并显示
            st.markdown("### Social Network Visualization")
            with st.spinner('Generating network graph...'):
                network_html_path = create_project_network(project_id, org_df)

            # 直接读取并显示生成的网络图
            with open(network_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=600, scrolling=True)

    # 控制台状态提示
    # print("✅ app.py is running the latest version")


