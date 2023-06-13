
# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#-------------------------------------------------------
# Import Dataset
Vaccination_PerCountry = pd.read_csv("Immunization 2021.csv", encoding='latin1')
Global_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='regional_global', encoding='latin1')
BCG_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='BCG', encoding='latin1')
DTP1_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='DTP1', encoding='latin1')
DTP3_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='DTP3', encoding='latin1')
HEPB3_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='HEPB3', encoding='latin1')
HIB3_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='HIB3', encoding='latin1')
MCV1_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='MCV1', encoding='latin1')
MCV2_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='MCV2', encoding='latin1')
POL3_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='POL3', encoding='latin1')
PCV3_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='PCV3', encoding='latin1')
ROTAC_PerCountry = pd.read_excel("Vaccines_per_Country_Year.xlsx", sheet_name='ROTAC', encoding='latin1')
survey_data = pd.read_excel("surveydata.xlsx", sheet_name='Coverage_survey', encoding='latin1')
#-------------------------------------------------------
# Set up the navigation menu
nav_selection = st.sidebar.radio("Menu", ["Global Vaccination Coverage 2021", "Vaccination Coverage by Year & Region", "Vaccination Coverage by Age & Gender"])

# Handle navigation selection
if nav_selection == "Global Vaccination Coverage 2021":

    #-------------------------------------------------------
    # Create a Streamlit map using Folium
    def create_map(data, selected_country=None):
        
        # Filter data based on selected country
        if selected_country:
            filtered_data = data[data['Countries and areas'] == selected_country]
        else:
            filtered_data = data
            
        # Create a base map centered on the mean of latitude and longitude coordinates
        map_center = [data['Latitude'].mean(), data['Longitude'].mean()]
        folium_map = folium.Map(location=map_center, zoom_start=4)
    
        # Create a marker cluster
        marker_cluster = MarkerCluster().add_to(folium_map)
    
        # Add markers for each country with hover information
        for index, row in data.iterrows():
            country = row['Countries and areas']
            percentages = {
                'BCG': row['BCG'],
                'DTP1': row['DTP1'],
                'DTP3': row['DTP3'],
                'Polio3': row['Polio3'],
                'MCV1': row['MCV1'],
                'MCV2(F)': row['MCV2 (F)'],
                'HepB3': row['HepB3'],
                'Hib3': row['Hib3'],
                'Rota': row['Rota'],
                'PCV3': row['PCV3'],
            }
            hover_text = f"Country: {country}<br>Vaccination Percentages:<br>"
            hover_text += "<ul>"
            for key, value in percentages.items():
                if pd.notnull(value):
                    hover_text += f"<li>{key}: {value}</li>"
                else:
                    hover_text += f"<li>{key}: None</li>"
            hover_text += "</ul>"
    
            # Create a marker and add it to the marker cluster
            marker = folium.Marker(
                location=(row['Latitude'], row['Longitude']),
                popup=hover_text,
            )
            marker.add_to(marker_cluster)
    
        return folium_map
    #-------------------------------------------------------
    # KPI: Number of countries where all vaccines where received
    kpi_value_1 = Vaccination_PerCountry['All Immunization Received?'].eq('Yes').sum()
    # Total Number of countries
    total_countries = len(Vaccination_PerCountry)
    
    #-------------------------------------------------------
    # KPI: List of countries with the highest percentages of vaccinations
    # Specify the columns of interest
    columns_of_interest = ['BCG', 'DTP1', 'DTP3', 'Polio3', 'MCV1', 'MCV2 (F)', 'HepB3', 'Hib3', 'Rota', 'PCV3']
    
    # Filter the DataFrame to include rows where "All Immunization Received?" is "Yes"
    filtered_df = Vaccination_PerCountry[Vaccination_PerCountry['All Immunization Received?'] == 'Yes']
    
    # Sort the DataFrame based on the columns of interest in descending order
    sorted_df = filtered_df.sort_values(columns_of_interest, ascending=False)
    
    # Get the top 10 countries
    top_10_countries = sorted_df['Countries and areas'].head(10).tolist()
    
    
    #-------------------------------------------------------
    # KPI: Number of countries with zero-doses
    count_blank_countries = Vaccination_PerCountry[Vaccination_PerCountry[columns_of_interest].isnull().all(axis=1)].shape[0]
    #-------------------------------------------------------
    # KPI: BCG lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    bcg_scores = Vaccination_PerCountry['BCG']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_BCG = Vaccination_PerCountry.loc[bcg_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: DTP1 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    dtp1_scores = Vaccination_PerCountry['DTP1']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_DTP1 = Vaccination_PerCountry.loc[dtp1_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: DTP3 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    dtp3_scores = Vaccination_PerCountry['DTP3']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_DTP3 = Vaccination_PerCountry.loc[dtp3_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: Polio3 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    polio3_scores = Vaccination_PerCountry['Polio3']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_Polio3 = Vaccination_PerCountry.loc[polio3_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: MCV1 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    MCV1_scores = Vaccination_PerCountry['MCV1']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_MCV1 = Vaccination_PerCountry.loc[MCV1_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: MCV2 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    MCV2_scores = Vaccination_PerCountry['MCV2 (F)']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_MCV2 = Vaccination_PerCountry.loc[MCV2_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: HepB3 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    HepB3_scores = Vaccination_PerCountry['HepB3']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_HepB3 = Vaccination_PerCountry.loc[HepB3_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: Hib3 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    Hib3_scores = Vaccination_PerCountry['Hib3']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_Hib3 = Vaccination_PerCountry.loc[Hib3_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: Rota lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    Rota_scores = Vaccination_PerCountry['Rota']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_Rota = Vaccination_PerCountry.loc[Rota_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    # KPI: PCV3 lowest
    # Filter the DataFrame to include only the BCG column and exclude empty or blank values
    PCV3_scores = Vaccination_PerCountry['PCV3']
    # Find the country with the lowest score in the filtered BCG scores
    lowest_country_PCV3 = Vaccination_PerCountry.loc[PCV3_scores.idxmin(), 'Countries and areas']
    #-------------------------------------------------------
    
    # Component 1
    st.markdown("<h1 style='color: #6B8E4E;'>Immunization Coverage of Preventable Diseases - Year 2021</h1>", unsafe_allow_html=True)
    # Add content for Component 1
    def main():
        
        # Add the country filter
        selected_country = st.selectbox("Select a country", ['All'] + list(Vaccination_PerCountry['Countries and areas'].unique()))
    
        # Filter data based on selected country
        if selected_country == 'All':
            filtered_data = Vaccination_PerCountry
        else:
            filtered_data = Vaccination_PerCountry[Vaccination_PerCountry['Countries and areas'] == selected_country]
    
        # Create the map and display it
        folium_map = create_map(filtered_data, selected_country)
        folium_static(folium_map)
    
    #-------------------------------------------------------      
        # Define the CSS style for the box
        box_style = """
            <style>
                .kpi-box {
                    background-color: #f8f8f8;
                    padding: 20px;
                    border-radius: 5px;
                    text-align: center;
                }
                .kpi-number {
                    color: #6B8E4E;
                    font-size: 24px;
                    margin-bottom: 5px;
                }
                .kpi-label {
                    font-size: 12px;
                }
            
                .kpi-number1 {
                    color: #AD5858;
                    font-size: 16px;
                    margin-bottom: 5px;
                }
            </style>
        """
    
        # Render the custom CSS styles
        st.markdown(box_style, unsafe_allow_html=True)
        
        # Display the 1st KPI
        st.markdown(
            f"""
            <div class='kpi-box' style='margin-bottom: 20px;'>
                <div class='kpi-number'><strong>{kpi_value_1}/{total_countries}</strong></div>
                <div class='kpi-label'><strong>Count of Countries with All Vaccines Completed</strong></div>
            </div>
            """,
            unsafe_allow_html=True)
        
        # Display the 2nd KPI
        st.markdown(
            f"""
            <div class='kpi-box' style='margin-bottom: 20px;'>
                <div class='kpi-number1' style='column-count: 2; text-align: center;'><strong>
                    {''.join(f"<div>{i}. {country}</div>" for i, country in enumerate(top_10_countries, start=1))}
                </strong></div>
                <div class='kpi-label'><strong>Top 10 Countries with the Highest Immunization Percentages</strong></div>
            </div>
            """,
            unsafe_allow_html=True)
        
            # Display the 3rd KPI
        st.markdown(
            f"""
            <div class='kpi-box' style='margin-bottom: 20px;'>
                <div class='kpi-number'><strong>{count_blank_countries}/{total_countries}</strong></div>
                <div class='kpi-label'><strong>Count of Countries with Zero-doses Given</strong></div>
            </div>
            """,
            unsafe_allow_html=True)
    
        #lowest vaccination%
        st.markdown(
            f"""
            <div class='kpi-box' style='display: flex;'>
                <div class='kpi-box-inner' style='flex: 1; margin-right: 20px;'>
                    <div class='kpi-number1'><strong>{lowest_country_BCG}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest BCG %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_DTP1}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest DTP1 %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_DTP3}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest DTP3 %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_MCV1}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest MCV1 %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_MCV2}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest MCV2 %</strong></div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True)
        
        #lowest vaccination%
        st.markdown(
            f"""
            <div class='kpi-box' style='display: flex;'>
                <div class='kpi-box-inner' style='flex: 1; margin-right: 20px;'>
                    <div class='kpi-number1'><strong>{lowest_country_HepB3}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest HepB3 %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_Hib3}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest Hib3 %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_Rota}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest Rota %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_PCV3}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest PCV3 %</strong></div>
                </div>
                <div class='kpi-box-inner' style='flex: 1;'>
                    <div class='kpi-number1'><strong>{lowest_country_Polio3}</strong></div>
                    <div class='kpi-label'><strong>Country with the lowest Polio3 %</strong></div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True)
    #-------------------------------------------------------   
        # Display the legend using Streamlit's HTML component
        st.markdown(
            """
            <style>
            .legend-container {
                width: 100%;
                margin-top: 20px;
                padding: 10px;
                background-color: #f8f8f8;
                border-radius: 5px;
                font-size: 13px;
            }
            .legend-item {
                display: flex;
                align-items: center;
                margin-bottom: 5px;
            }
            </style>
            """
            "<div class='legend-container'>"
            "<p><strong>Legend</strong></p>"
            "<div class='legend-item'><span>BCG – Percentage of live births who received bacilli Calmette−Guérin (vaccine against tuberculosis)</span></div>"
            "<div class='legend-item'><span>DTP1 – Percentage of surviving infants who received the first dose of diphtheria, pertussis and tetanus vaccine</span></div>"
            "<div class='legend-item'><span>DTP3 – Percentage of surviving infants who received three doses of diphtheria, pertussis and tetanus vaccine</span></div>"
            "<div class='legend-item'><span>Polio3 – Percentage of surviving infants who received three doses of the polio vaccine</span></div>"
            "<div class='legend-item'><span>MCV1 – Percentage of surviving infants who received the first dose of the measles−containing vaccine</span></div>"
            "<div class='legend-item'><span>MCV2 – Percentage of children who received the second dose of measles−containing vaccine as per national schedule</span></div>"
            "<div class='legend-item'><span>HepB3 – Percentage of surviving infants who received three doses of hepatitis B vaccine</span></div>"
            "<div class='legend-item'><span>Hib3 – Percentage of surviving infants who received three doses of Haemophilus influenzae type b vaccine</span></div>"
            "<div class='legend-item'><span>Rota – Percentage of surviving infants who received the last dose of rotavirus vaccine as recommended</span></div>"
            "<div class='legend-item'><span>PCV3 – Percentage of surviving infants who received three doses of pneumococcal conjugate vaccine</span></div>"
            "</div>",
            unsafe_allow_html=True)
            
    # Display the Home page
    if __name__ == '__main__':
        main() 

#-------------------------------------------------------
elif nav_selection == "Vaccination Coverage by Year & Region":

    # Set up the Streamlit application
    st.markdown("<h1 style='color: #6B8E4E;'>Vaccine Coverage</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #B2C5B2;'>Bar chart showing the coverage percentage for the selected vaccine by year and region.</h3>", unsafe_allow_html=True)
    
    # Group the DataFrame by vaccine type
    grouped = Global_PerCountry.groupby('vaccine')
    
    # Get the unique vaccine types
    vaccine_types = Global_PerCountry['vaccine'].unique()
    
    # Add a selectbox widget for the vaccine filter
    selected_vaccine = st.selectbox('Select Vaccine', vaccine_types)
    
    # Filter the DataFrame for the selected vaccine
    filtered_data = Global_PerCountry[Global_PerCountry['vaccine'] == selected_vaccine]
    
    # Group the filtered DataFrame by region
    grouped_by_region = filtered_data.groupby('region')
    
    # Create a bar chart for each region
    fig = go.Figure()
    
    region_colors = {}  # Color mapping dictionary
    
    for region, group in grouped_by_region:
        # Sort the group by year
        sorted_group = group.sort_values('year')
    
        # Add a new column for change in coverage from year to year
        sorted_group['change'] = sorted_group['coverage'].diff()
    
        # Add a trace for the region to the stacked bar chart
        fig.add_trace(go.Bar(
            x=sorted_group['year'],
            y=sorted_group['coverage'],
            name=region
        ))
    
        region_colors[region] = len(fig.data) - 1  # Assign a unique color index to each region
    
    # Specify the range of x-axis
    fig.update_xaxes(range=[2000, 2021])
    
    # Set the title color using HTML styling
    title = f'<span style="color:#6B8E4E">{selected_vaccine} Coverage by Region</span>'
    
    # Update the title of the bar chart
    fig.update_layout(
        title=title,
        barmode='stack',  # Set the barmode to 'stack' for stacked bars
        legend=dict(
            title='Region',
            traceorder='normal',
            tracegroupgap=0  # Ensure consistent color per region in the legend
        )
    )
    
    # Set consistent colors in the legend
    for i, legend_item in enumerate(fig.data):
        legend_item.marker.color = region_colors[legend_item.name]
    
    # Display the bar chart using Streamlit
    st.plotly_chart(fig)
    
    #-----------------------------------------------------
    st.markdown("<h1 style='color: #6B8E4E;'>Zero-doses</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #B2C5B2;'>Bar chart showing the non-coverage percentage for the selected vaccine by year and region.</h3>", unsafe_allow_html=True)
    # Define the years and UNICEF regions
    years = [str(year) for year in range(2021, 1999, -1)]
    unicef_regions = BCG_PerCountry['unicef_region'].unique()
    
    # Create a dictionary to store the data for each vaccine
    vaccines = {
        'BCG': BCG_PerCountry,
        'DTP1': DTP1_PerCountry,
        'DTP3': DTP3_PerCountry,
        'HEPB3': HEPB3_PerCountry,
        'MCV1': MCV1_PerCountry,
        'MCV2': MCV2_PerCountry,
        'POL3': POL3_PerCountry,
        'PCV3': PCV3_PerCountry,
        'ROTAC': ROTAC_PerCountry,
        'HIB3': HIB3_PerCountry
    }
    
    # Global filter
    selected_vaccine = st.selectbox('Select a vaccine', list(vaccines.keys()))
    
    # Create a dictionary to store the counts of blank values by UNICEF region and year
    blank_counts = {}
    
    # Calculate the number of blank values for each year and UNICEF region
    for year in years:
        blank_counts[year] = {}
        for region in unicef_regions:
            count = vaccines[selected_vaccine][(vaccines[selected_vaccine]['unicef_region'] == region)][year].isnull().sum()
            blank_counts[year][region] = count
    
    # Create a DataFrame from the blank_counts dictionary
    blank_counts_df = pd.DataFrame(blank_counts)
    
    # Create the stacked bar plot
    fig = go.Figure()
    
    for region in unicef_regions:
        fig.add_trace(go.Bar(
            x=years,
            y=blank_counts_df.loc[region],
            name=region,
            marker=dict(color=region_colors[region])  # Use consistent color per region
        ))
    
    fig.update_layout(
        barmode='stack',
        title=f'<span style="color:#6B8E4E">Zero-dose {selected_vaccine} by UNICEF Region and Year</span>',
        xaxis_title='Year',
        yaxis_title='Count',
        legend_title='UNICEF Region',
        legend=dict(
            title='Region',
            traceorder='normal',
            tracegroupgap=0  # Ensure consistent color per region in the legend
        )
    )
    
    # Set consistent colors in the legend
    for i, legend_item in enumerate(fig.data):
        legend_item.marker.color = region_colors[legend_item.name]
    
    # Display the plot using Streamlit
    st.plotly_chart(fig, use_container_width=True)
        
    #---------------------------------------------------------
    #Treemap
    # Filter the years equal to or above 2000 and sort them in descending order
    years = sorted(Global_PerCountry['year'].unique(), reverse=True)
    years = [year for year in years if year >= 2000]
    
    # Global filters
    selected_year = st.selectbox('Select Year', years, key='year_filter')
    selected_region = st.selectbox('Select Region', Global_PerCountry['region'].unique(), key='region_filter')
    
    # Filter the data based on the selected year and region
    filtered_data = Global_PerCountry[(Global_PerCountry['year'] == selected_year) & (Global_PerCountry['region'] == selected_region)]
    
    # Calculate the coverage proportion as a percentage
    filtered_data['coverage_percentage'] = filtered_data['coverage'] * 100
    
    # Create a treemap
    fig = px.treemap(filtered_data,
                     path=['vaccine'],
                     values='coverage_percentage',
                     color='coverage_percentage',
                     color_continuous_scale='Viridis',
                     title=f'Vaccine Coverage Proportion ({selected_year}, {selected_region})')
    
    # Update the layout
    fig.update_layout(margin={'r': 10, 't': 50, 'l': 10, 'b': 10})
    
    # Display the treemap using Streamlit
    st.plotly_chart(fig)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #-------------------------------------------------------
    # Display the legend using Streamlit's HTML component
    st.markdown(
        """
        <style>
        .legend-container {
            width: 100%;
            margin-top: 20px;
            padding: 10px;
            background-color: #f8f8f8;
            border-radius: 5px;
            font-size: 13px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        </style>
        """
        "<div class='legend-container'>"
        "<p><strong>Legend</strong></p>"
        "<div class='legend-item'><span>BCG – Percentage of live births who received bacilli Calmette−Guérin (vaccine against tuberculosis)</span></div>"
        "<div class='legend-item'><span>DTP1 – Percentage of surviving infants who received the first dose of diphtheria, pertussis and tetanus vaccine</span></div>"
        "<div class='legend-item'><span>DTP3 – Percentage of surviving infants who received three doses of diphtheria, pertussis and tetanus vaccine</span></div>"
        "<div class='legend-item'><span>Polio3 – Percentage of surviving infants who received three doses of the polio vaccine</span></div>"
        "<div class='legend-item'><span>MCV1 – Percentage of surviving infants who received the first dose of the measles−containing vaccine</span></div>"
        "<div class='legend-item'><span>MCV2 – Percentage of children who received the second dose of measles−containing vaccine as per national schedule</span></div>"
        "<div class='legend-item'><span>HepB3 – Percentage of surviving infants who received three doses of hepatitis B vaccine</span></div>"
        "<div class='legend-item'><span>Hib3 – Percentage of surviving infants who received three doses of Haemophilus influenzae type b vaccine</span></div>"
        "<div class='legend-item'><span>Rota – Percentage of surviving infants who received the last dose of rotavirus vaccine as recommended</span></div>"
        "<div class='legend-item'><span>PCV3 – Percentage of surviving infants who received three doses of pneumococcal conjugate vaccine</span></div>"
        "</div>",
        unsafe_allow_html=True)

        
#-------------------------------------------------------
elif nav_selection == "Vaccination Coverage by Age & Gender":
    st.markdown("<h1 style='color: #6B8E4E;'>Vaccination per Age</h1>", unsafe_allow_html=True)

    # Filter out rows with blank values in coverage and sex_male/sex_female
    filtered_data = survey_data.dropna(subset=['coverage','sex_male','sex_female'])
    
    # Get unique values for cohortYear and vaccine
    cohort_years = filtered_data['cohortYear'].unique()
    vaccines = filtered_data['vaccine'].unique()
    
    # Filter the cohort years from 2000 to 2020
    cohort_years = [year for year in cohort_years if 2000 <= year <= 2020]
    cohort_years.sort(reverse=True)  # Sort the years in descending order
    
    # Add "All Years" to cohort_years
    cohort_years.insert(0, "All Years")
    
    # Add "All Vaccines" to vaccines
    vaccines = np.append("All Vaccines", vaccines)
    
    # Global filters
    selected_cohort_year = st.selectbox('Select Year', cohort_years)
    selected_vaccine = st.selectbox('Select Vaccine', vaccines)
    
    # Apply filters if specific year/vaccine is selected
    if selected_cohort_year != "All Years":
        filtered_data = filtered_data[filtered_data['cohortYear'] == selected_cohort_year]
    
    if selected_vaccine != "All Vaccines":
        filtered_data = filtered_data[filtered_data['vaccine'] == selected_vaccine]
    
    # Convert sex_male and sex_female columns to numeric
    filtered_data['sex_male'] = pd.to_numeric(filtered_data['sex_male'], errors='coerce')
    filtered_data['sex_male'].fillna(-1, inplace=True)
    
    filtered_data['sex_female'] = pd.to_numeric(filtered_data['sex_female'], errors='coerce')
    filtered_data['sex_female'].fillna(-1, inplace=True)
    
    # Define the coverage categories
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    # Categorize the coverage values
    filtered_data['coverage_category'] = pd.cut(filtered_data['coverage'], bins=bins, labels=labels)
    
    # Calculate the sums for each coverage category and sex
    grouped_data = filtered_data.groupby(['coverage_category']).agg({'sex_male': 'sum', 'sex_female': 'sum'}).reset_index()
    
    
    # Calculate the values for the pyramid chart
    male_values = grouped_data['sex_male'].values[::-1]
    female_values = grouped_data['sex_female'].values
    
    # Create the pyramid chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=labels,
        x=male_values,
        name='Male',
        orientation='h',
        marker=dict(color='skyblue')
    ))
    
    fig.add_trace(go.Bar(
        y=labels,
        x=female_values * -1,
        name='Female',
        orientation='h',
        marker=dict(color='pink')
    ))
    
    fig.update_layout(
        template='plotly_white',
        title='Vaccination Coverage Pyramid by Sex',
        title_font_size=24,
        barmode='relative',
        bargap=0,
        bargroupgap=0,
        xaxis=dict(
            tickmode='array',
            tickvals=[-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100],
            ticktext=[100, 80, 60, 40, 20, 0, 20, 40, 60, 80, 100],
            title='Count',
        ),
        yaxis=dict(title='Coverage Category')
    )
    
    # Display the pyramid chart using Streamlit
    st.plotly_chart(fig)



    # Group the data by age category and calculate the average coverage
    grouped_data = filtered_data.groupby('ageVaccination')['coverage'].mean().reset_index()
    
    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(grouped_data['ageVaccination'], grouped_data['coverage'])
    plt.xlabel('Age Category')
    plt.ylabel('Coverage')
    plt.title('Age Category vs. Coverage')
    
    # Rotate the x-axis labels for better visibility
    plt.xticks(rotation=45)
    
    # Display the bar chart using Streamlit
    st.pyplot(plt)

    
#-------------------------------------------------------   
    # Display the legend using Streamlit's HTML component
    st.markdown(
        """
        <style>
        .legend-container {
            width: 100%;
            margin-top: 20px;
            padding: 10px;
            background-color: #f8f8f8;
            border-radius: 5px;
            font-size: 13px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        </style>
        """
        "<div class='legend-container'>"
        "<p><strong>Legend</strong></p>"
        "<div class='legend-item'><span>BCG – Percentage of live births who received bacilli Calmette−Guérin (vaccine against tuberculosis)</span></div>"
        "<div class='legend-item'><span>DTP1 – Percentage of surviving infants who received the first dose of diphtheria, pertussis and tetanus vaccine</span></div>"
        "<div class='legend-item'><span>DTP3 – Percentage of surviving infants who received three doses of diphtheria, pertussis and tetanus vaccine</span></div>"
        "<div class='legend-item'><span>Polio3 – Percentage of surviving infants who received three doses of the polio vaccine</span></div>"
        "<div class='legend-item'><span>MCV1 – Percentage of surviving infants who received the first dose of the measles−containing vaccine</span></div>"
        "<div class='legend-item'><span>MCV2 – Percentage of children who received the second dose of measles−containing vaccine as per national schedule</span></div>"
        "<div class='legend-item'><span>HepB3 – Percentage of surviving infants who received three doses of hepatitis B vaccine</span></div>"
        "<div class='legend-item'><span>Hib3 – Percentage of surviving infants who received three doses of Haemophilus influenzae type b vaccine</span></div>"
        "<div class='legend-item'><span>Rota – Percentage of surviving infants who received the last dose of rotavirus vaccine as recommended</span></div>"
        "<div class='legend-item'><span>PCV3 – Percentage of surviving infants who received three doses of pneumococcal conjugate vaccine</span></div>"
        "</div>",
        unsafe_allow_html=True)
