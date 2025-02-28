import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

df = pd.read_csv('india.csv')

list_of_states = list(df['State'].unique())
list_of_states.insert(0,'Overall India')
list_analysis = {
    'Demographic & Social Profile': df[['Population','sex_ratio','literacy_rate','Male', 'Female','Literate', 'Male_Literate', 'Female_Literate','Age not stated','Age_Group_0_29','Age_Group_30_49','Age_Group_50',
                                    'SC', 'Male_SC', 'Female_SC','ST', 'Male_ST', 'Female_ST'
                                    ,'Hindus','Muslims','Christians','Sikhs','Buddhists','Jains','Religion_Not_Stated']],
    'Economic & Employment Analysis': df[['Workers','Male_Workers','Female_Workers','Main_Workers','Marginal_Workers','Non_Workers','Cultivator_Workers','Agricultural_Workers','Household_Workers','Other_Workers',
                                        'Power_Parity_Less_than_Rs_45000','Power_Parity_Rs_45000_90000','Power_Parity_Rs_90000_150000','Power_Parity_Rs_45000_150000','Power_Parity_Rs_150000_240000',
                                        'Power_Parity_Rs_240000_330000','Power_Parity_Rs_150000_330000','Power_Parity_Rs_330000_425000','Power_Parity_Rs_425000_545000','Power_Parity_Rs_330000_545000','Power_Parity_Above_Rs_545000','Total_Power_Parity']],
    'Household & Infrastructure Overview' : df[['Households','LPG_or_PNG_Households', 'Rural_Households','Urban_Households','Households_with_Internet','Households_with_Computer','Households_with_Bicycle','Households_with_Car_Jeep_Van','Households_with_Scooter_Motorcycle_Moped',
                                                'Condition_of_occupied_census_houses_Dilapidated_Households','Households_with_separate_kitchen_Cooking_inside_house','Having_bathing_facility_Total_Households','Having_latrine_facility_within_the_premises_Total_Households','Ownership_Owned_Households','Ownership_Rented_Households']],
    'Education & Household Characteristics':df[['Below_Primary_Education','Primary_Education','Middle_Education','Secondary_Education','Higher_Education','Graduate_Education','Other_Education','Literate_Education','Illiterate_Education','Total_Education',
                                                'Household_size_1_person_Households','Household_size_2_persons_Households','Household_size_3_persons_Households','Household_size_4_persons_Households','Married_couples_1_Households','Married_couples_2_Households','Married_couples_3_or_more_Households']],
    'Water, Sanitation & Utilities' : df[['Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households','Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households','Main_source_of_drinking_water_Tapwater_Households','Main_source_of_drinking_water_Tubewell_Borehole_Households','Main_source_of_drinking_water_Un_covered_well_Households',
                                          'Location_of_drinking_water_source_Away_Households','Location_of_drinking_water_source_Near_the_premises_Households','Location_of_drinking_water_source_Within_the_premises_Households']]
    }

def select(data_dict, primary_key):
    if primary_key not in data_dict:
        valid_keys = list(data_dict.keys())
        raise ValueError(f"Invalid key '{primary_key}'. Valid options: {valid_keys}")
    return data_dict[primary_key].columns.tolist()

def selectsecondary(primary_key,list_analysiss):
    sec = None
    if primary_key == 'Demographic & Social Profile':
         sec = df[['Population','sex_ratio','literacy_rate','Male', 'Female','Literate', 'Male_Literate','SC', 'Male_SC', 'Female_SC','ST', 'Male_ST', 'Female_ST']]
    elif primary_key =='Water, Sanitation & Utilities':
         sec = df[['Location_of_drinking_water_source_Away_Households','Location_of_drinking_water_source_Near_the_premises_Households','Location_of_drinking_water_source_Within_the_premises_Households']]
    elif primary_key =='Economic & Employment Analysis':
         sec = df[['Workers','Male_Workers','Female_Workers','Main_Workers','Marginal_Workers','Non_Workers','Cultivator_Workers','Agricultural_Workers','Household_Workers','Other_Workers']]
    elif primary_key =='Household & Infrastructure Overview':
         sec = df[['Households','LPG_or_PNG_Households', 'Rural_Households','Urban_Households']]
    elif primary_key =='Education & Household Characteristics':
         sec= df[['Below_Primary_Education','Primary_Education','Middle_Education','Secondary_Education','Higher_Education','Graduate_Education','Other_Education','Literate_Education','Illiterate_Education','Total_Education']]

    return sorted(sec)
st.sidebar.title('India Data Viz')
selected_state = st.sidebar.selectbox('Select a state',list_of_states)
# In sidebar
primary = st.sidebar.selectbox('Analysis Parameter', list_analysis.keys())
secondary = st.sidebar.selectbox('select size Parameter',selectsecondary(primary,list_analysis))
Tertiary = st.sidebar.selectbox('Select color Parameter',select(list_analysis, primary))
# parameter = st.sidebar.selectbox('Select color Parameter',select(list_analysis, primary))
plot = st.sidebar.button('Plot Graph')

if plot:


    st.markdown("<h1 style='text-align: center; color: white;'>India Data Viz </h1>",
                unsafe_allow_html=True)
    if selected_state == 'Overall India':
        # plot for india
        st.subheader('India State wise')
        fig1 = px.scatter_mapbox(df, lat="Latitude_y", lon="Longitude_y", size=secondary, color=Tertiary, zoom=4,
                                 size_max=35,
                                 mapbox_style="carto-positron", width=1200, height=700, hover_name='State')

        st.plotly_chart(fig1, use_container_width=True)

        st.subheader('India District wise')
        fig = px.scatter_mapbox(df, lat="Latitude_x", lon="Longitude_x", size=secondary, color=Tertiary, zoom=4,
                                size_max=35,
                                mapbox_style="carto-positron", width=1200, height=700, hover_name='District')

        st.plotly_chart(fig, use_container_width=True)

    else:
        # plot for state
        st.subheader('India District wise')
        state_df = df[df['State'] == selected_state]

        fig = px.scatter_mapbox(state_df, lat="Latitude_x", lon="Longitude_x", size=secondary, color=Tertiary, zoom=6, size_max=35,
                                mapbox_style="carto-positron", width=1200, height=700,hover_name='District')

        st.plotly_chart(fig, use_container_width=True)