import streamlit as st
from searcher import search_projects
from create_network import create_project_network
import pandas as pd
from rag_app import Retriever, chat_app

def app():
    
    if "selected_project_id" not in st.session_state:
        st.title("Explore your projects")
        st.session_state.selected_project_id = None
    if "page" not in st.session_state:
        st.session_state.page = "🔍 Search"
    if "latest_results" not in st.session_state:
        st.session_state.latest_results = []


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

                if st.button(f"View Details: {r['projectID']}", key=f"view_{r['projectID']}_{index}"):
                    st.session_state.selected_project_id = r['projectID']
                    st.session_state.page = "📄 Project Detail"

    # 详情页
    elif st.session_state.page == "📄 Project Detail":
        
        # 获取选中的项目 ID
        project_id = st.session_state.selected_project_id        

        filtered_project = pd.read_csv('project_geo.csv', encoding="utf-8-sig")
        filtered_project['projectID'] = filtered_project['projectID'].astype(str)
        
        
        if filtered_project.empty:
            st.error(f"No project found with Project ID: {project_id}")
            st.stop()  # 停止执行后续代码
        project = filtered_project[filtered_project['projectID'] == project_id].to_dict('records')[0]
        st.title(f"📄 {project['acronym']}")
        st.subheader(f"{project['title']}")    
        st.markdown(f"""
        **Status:** {project['status']}  
        **Duration:** {project['startDate']} to {project['endDate']}  
        **Total Cost:** €{project['totalCost']}  
        **EU Contribution:** €{project['ecMaxContribution']}  
        **Topics:** {project['topics']}  
        **Funding Scheme:** {project['fundingScheme']}
        **[DOI](https://doi.org/{project['grantDoi']})**
        """)
        with st.sidebar:
            chat_app(int(project_id), project['title'], project['objective'])
        st.markdown("### Project Objective")
        st.write(project['objective'])
        st.markdown("### Participating Organisations")
        org_df = pd.read_csv('organization.csv', encoding="utf-8-sig") 
        org_df['projectID'] = org_df['projectID'].astype(str)
        
        participating_orgs = org_df[org_df['projectID'] == project_id]
        
        if participating_orgs.empty:
            st.warning("No participating organizations found for this project.")
        else:                
            participating_orgs_display = participating_orgs[['name', 'country', 'activityType', 'city', 'SME', 'role', 'organizationURL']].reset_index(drop=True)
            st.dataframe(participating_orgs_display.set_index('name').sort_values(by='role',ascending=False), use_container_width=True)
            
        st.markdown("### Social Network Visualization")
        with st.spinner('Generating network graph...'):
            html_content = create_project_network(project_id, org_df)

        st.components.v1.html(html_content, height=500, scrolling=True)
        st.markdown("### Similar Projects")
        st.write("These projects are similar to the one you are currently viewing. You can explore them further.")
        
        similar_projects = Retriever().get_similar_project(int(project_id))
        similar_projects = pd.DataFrame(similar_projects)
        similar_projects['similar_project_id'] = similar_projects['similar_project_id'].astype(str)
        similar_projects.set_index('similar_project_id', inplace=True)
        st.dataframe(similar_projects.rename(columns={'similar_project_id':'Project ID','title':"Title"}), use_container_width=True)

