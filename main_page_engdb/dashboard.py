import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

def app():
    st.title("Welcome to the Dashboard Page")
    # st.write("This is the Dashboard section.")
    # Page configuration
    #st.set_page_config(layout="wide")

    # European countries list (keep your original definition)
    european_countries = [
        'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 
        'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
        'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 
        'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy',
        'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
        'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands',
        'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania',
        'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom',
        'Vatican City'
    ]

    # Country mapping (keep your original definition)
    country_mapping = {
        'NL': 'Netherlands', 'DK': 'Denmark', 'DE': 'Germany', 'ES': 'Spain', 
        'EL': 'Greece', 'IT': 'Italy', 'UA': 'Ukraine', 'PL': 'Poland', 
        'SE': 'Sweden', 'NO': 'Norway', 'SK': 'Slovakia', 'FR': 'France', 
        'BE': 'Belgium', 'SI': 'Slovenia', 'UK': 'United Kingdom', 'FI': 'Finland',
        'HU': 'Hungary', 'PT': 'Portugal', 'LT': 'Lithuania', 'BG': 'Bulgaria', 
        'EE': 'Estonia', 'LV': 'Latvia', 'RO': 'Romania', 'AT': 'Austria', 
        'HR': 'Croatia', 'IE': 'Ireland', 'MT': 'Malta', 'RS': 'Serbia', 
        'CZ': 'Czech Republic', 'CY': 'Cyprus', 'CH': 'Switzerland', 
        'IS': 'Iceland', 'LU': 'Luxembourg', 'ME': 'Montenegro', 'MD': 'Moldova',
        'MK': 'North Macedonia', 'LI': 'Liechtenstein', 'AD': 'Andorra',
        'MC': 'Monaco', 'VA': 'Vatican City', 'SM': 'San Marino', 'XK': 'Kosovo'
    }

    # Country coordinates (keep your original definition)
    country_coords = {
        'Netherlands': [52.3784, 4.9009], 'Denmark': [55.6761, 12.5683], 
        'Germany': [51.1657, 10.4515], 'Spain': [40.4637, -3.7492],
        'Greece': [39.0742, 21.8243], 'Italy': [41.8719, 12.5674], 
        'Ukraine': [48.3794, 31.1656], 'Poland': [51.9194, 19.1451], 
        'Sweden': [60.1282, 18.6435], 'Norway': [60.4720, 8.4689], 
        'Slovakia': [48.6690, 19.6990], 'France': [46.6034, 1.8883], 
        'Belgium': [50.8503, 4.3517], 'Slovenia': [46.1511, 14.9955], 
        'United Kingdom': [55.3781, -3.4360], 'Finland': [61.9241, 25.7482], 
        'Hungary': [47.1625, 19.5033], 'Portugal': [39.3999, -8.2245], 
        'Lithuania': [55.1694, 23.8813], 'Bulgaria': [42.7339, 25.4858], 
        'Estonia': [58.5953, 25.0136], 'Latvia': [56.8796, 24.6032],
        'Romania': [45.9432, 24.9668], 'Austria': [47.5162, 14.5501], 
        'Croatia': [45.1, 15.2], 'Ireland': [53.1424, -7.6921],
        'Malta': [35.9375, 14.3754], 'Serbia': [44.0165, 21.0059], 
        'Czech Republic': [49.8175, 15.4730], 'Cyprus': [35.1264, 33.4299],
        'Switzerland': [46.8182, 8.2275], 'Iceland': [64.9631, -19.0208], 
        'Luxembourg': [49.6117, 6.13], 'Montenegro': [42.7087, 19.3744], 
        'Moldova': [47.0105, 28.8575], 'North Macedonia': [41.6086, 21.7453], 
        'Liechtenstein': [47.1415, 9.5215], 'Andorra': [42.5078, 1.5211],
        'Monaco': [43.7333, 7.4167], 'Vatican City': [41.9029, 12.4534],
        'San Marino': [43.9424, 12.4578], 'Kosovo': [42.6026, 20.9020],
        'Albania': [41.1533, 20.1683], 'Belarus': [53.7098, 27.9534],
        'Bosnia and Herzegovina': [43.9159, 17.6791], 'Russia': [61.5240, 105.3188]
    }


    # Load data - modified to preserve all original columns
    @st.cache_data
    def load_data():
        df = pd.read_csv("project_geo.csv")
        df['ecSignatureDate'] = pd.to_datetime(df['ecSignatureDate'], errors='coerce')
        return df
    
    df_europe = load_data()    

    # Country detail page - modified to show all columns
    def show_country_detail(country_name):
        st.subheader(f"📊 {country_name} - Project Details")
        # selected_cols = ['projectID','acronym', 'title', 'objective','endDate','status', 'totalCost', 'ecSignatureDate', 'ecMaxContribution']
        
        # Get country data with all original columns
        country_data = df_europe[df_europe['country'] == country_name]#[selected_cols].drop_duplicates()
        country_data.projectID = country_data.projectID.astype(str)
        # Basic info
        cols = st.columns(3)
        with cols[0]:
            st.metric("Total Projects", country_data['projectID'].nunique())
        
        with cols[1]:
            total_cost = country_data['totalCost'].sum()/1000000 
            st.metric("Total Cost (million EUR)", f"€{total_cost:,.2f}")

        with cols[2]:
            if 'ecSignatureDate' in country_data.columns:
                earliest_year = pd.to_datetime(country_data['ecSignatureDate']).min().year
                st.metric("Earliest Project Year", earliest_year)
            else:
                st.metric("Earliest Project Year", "Data not available")
        
        # Project distribution by year-month
        if 'ecSignatureDate' in country_data.columns:
            st.write("### Project Distribution by Year-Month")
            country_data['year_month'] = country_data['ecSignatureDate'].dt.to_period('M').astype(str)
            country_data = country_data[country_data['year_month'] != 'NaT']
            monthly_counts = country_data.groupby('year_month')['projectID'].nunique()
            
            tab1, tab2 = st.tabs(["Project Count", "Total Cost"])
            
            with tab1:
                st.bar_chart(monthly_counts)
            
            with tab2:
                if 'totalCost' in country_data.columns:
                    monthly_costs = country_data.groupby('year_month')['totalCost'].sum()
                    st.line_chart(monthly_costs)
                else:
                    st.warning("Total cost data not available for line chart")
        
        # Project list with all columns
        st.write("### Project Details")
        
        # Sorting options
        sort_col, filter_col = st.columns(2)
        
        with sort_col:
            sort_options = ['Default']
            if 'totalCost' in country_data.columns:
                sort_options.extend(['Total Cost (High to Low)', 'Total Cost (Low to High)'])
            if 'ecSignatureDate' in country_data.columns:
                sort_options.extend(['Date (Newest First)', 'Date (Oldest First)'])
            
            sort_by = st.selectbox("Sort by", sort_options)
            
            if sort_by == 'Total Cost (High to Low)':
                country_data = country_data.sort_values('totalCost', ascending=False)
            elif sort_by == 'Total Cost (Low to High)':
                country_data = country_data.sort_values('totalCost', ascending=True)
            elif sort_by == 'Date (Newest First)':
                country_data = country_data.sort_values('ecSignatureDate', ascending=False)
            elif sort_by == 'Date (Oldest First)':
                country_data = country_data.sort_values('ecSignatureDate', ascending=True)
        
        # Status filter
        with filter_col:
            if 'status' in country_data.columns:
                status_options = ['All'] + list(country_data['status'].unique())
                selected_status = st.selectbox("Filter by Status", status_options)
                if selected_status != 'All':
                    country_data = country_data[country_data['status'] == selected_status]
        # Display SELECTED columns from the original data
        
        show_cols = ['projectID','acronym', 'title', 'objective','endDate','status', 'project_totalCost', 'ecSignatureDate', 'ecMaxContribution']
        cols_label= ['Project ID', 'Acronym', 'Title', 'Objective', 'End Date', 'Status', 'Total Cost (EUR)', 'Signature Date', 'Max Contribution (EUR)']
        zip_cols = dict(zip(show_cols, cols_label))
        show_df = country_data[show_cols].drop_duplicates().rename(columns=zip_cols)
        
        st.dataframe(show_df, use_container_width=True)
        
        if st.button("← Back to Map"):
            st.session_state['selected_country'] = None
            st.rerun()

    # Main map page
    def show_main_map():
        st.title("🌍 European Research Project Distribution")
        
        # Count projects by country
        heat_data = pd.read_csv("country_count.csv")
        
        # Create map
        m = folium.Map(location=[54.5260, 15.2551], zoom_start=4, tiles='CartoDB positron')
        # Add heatmap
        
        HeatMap(heat_data[['lat','lng','count']], radius=20, blur=15, min_opacity=0.3, max_zoom=1).add_to(m)
        
        # Add clickable country markers
        for point in heat_data.to_dict(orient='records'):
            country = point['country']
            folium.Marker(
                location=[point['lat'], point['lng']],
                popup=folium.Popup(f"<b>{country}</b><br>{point['count']} projects", max_width=200),
                tooltip=f"Click for {country} details",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        
        # Display map and handle clicks
        map_data = st_folium(
            m, 
            width=1200, 
            height=600,
            returned_objects=["last_object_clicked", "last_object_clicked_popup"]
        )
        
        # Handle click events
        if map_data.get("last_object_clicked"):
            click_lat = map_data["last_object_clicked"]["lat"]
            click_lon = map_data["last_object_clicked"]["lng"]
            
            # Find nearest country
            min_distance = float('inf')
            selected_country = None
            for point in heat_data.to_dict(orient='records'):
                distance = (point['lat'] - click_lat)**2 + (point['lng'] - click_lon)**2
                if distance < min_distance:
                    min_distance = distance
                    selected_country = point['country']
        
            if selected_country and min_distance < 5:  # Reasonable distance threshold
                st.session_state['selected_country'] = selected_country
                st.rerun()
        
        # Show data table
        with st.expander("View Country Statistics"):
            st.dataframe(heat_data.sort_values('count', ascending=False), 
                        use_container_width=True)

    # Initialize session state
    if 'selected_country' not in st.session_state:
        st.session_state['selected_country'] = None

    # Display appropriate page
    if st.session_state['selected_country']:
        show_country_detail(st.session_state['selected_country'])
    else:
        show_main_map()