import streamlit as st

# Sample data: List of research projects
projects = [
    {"name": "Electricity Demand Forecasting", "description": "Analyzing patterns and building models for predicting electricity demand."},
    {"name": "Transport Punctuality Heatmap", "description": "Creating route-wise heatmaps for transport schedules."},
    {"name": "Climate Change Impact on Agriculture", "description": "Assessing climate change effects on crop yields and production."}
]

def main_page():
    """Displays the homepage with a list of projects."""
    st.title("Research Projects")
    st.write("Select a project to view more details.")

    # Display projects as clickable links
    for project in projects:
        if st.button(project["name"]):
            # Navigate to the sub-page with the selected project
            st.session_state.query_params = {"page": "project", "name": project["name"]}


def project_page():
    """Displays the details of a selected project."""
    query_params = st.session_state.get("query_params", {})
    project_name = query_params.get("name", None)  # Get the project name from session state

    if project_name:
        # Find the project details
        project = next((p for p in projects if p["name"] == project_name), None)
        if project:
            st.title(project["name"])
            st.write(project["description"])
            if st.button("Back to Projects"):
                st.session_state.query_params = {"page": "main"}
        else:
            st.error("Project not found.")
    else:
        st.error("No project selected.")

# Main logic: Determine which page to display
query_params = st.session_state.get("query_params", {"page": "main"})
page = query_params.get("page", "main")  # Default to "main" page

if page == "main":
    main_page()
elif page == "project":
    project_page()
else:
    st.error("Page not found.")
