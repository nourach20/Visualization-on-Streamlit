import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data
df = pd.read_csv('https://linked.aub.edu.lb/pkgcube/data/86dafba6d90f5865b6a218be00dc259f_20240908_130351.csv')

# Clean Reference Area feature
df['refArea_clean'] = df['refArea'].str.replace('https://dbpedia.org/page/', '', regex=False)
df['refArea_clean'] = df['refArea_clean'].str.replace('http://dbpedia.org/resource/', '', regex=False)

# ------------------ Internet Availability Bar Chart ------------------

# Melt the data to get internet availability status
df_internet_melted = df.melt(id_vars=['refArea_clean'],
                             value_vars=['Status of internet availability - available',
                                         'Status of internet availability - partially available ',
                                         'Status of internet availability - not available'],
                             var_name='Internet Availability', value_name='Count')

# Interactive Features for Bar Chart
st.title("Interactive Internet Availability Visualization")

# Slider for Bar Chart
min_count_bar = int(df_internet_melted['Count'].min())
max_count_bar = int(df_internet_melted['Count'].max())
slider_value_bar = st.slider("Select a minimum count value for Internet Availability", 
                             min_value=min_count_bar, 
                             max_value=max_count_bar, 
                             value=min_count_bar)

# Dropdown for Bar Chart
selected_status_bar = st.selectbox("Select Internet Availability Status to filter", 
                                   options=['All'] + df_internet_melted['Internet Availability'].unique().tolist())

# Filter the data for Bar Chart
filtered_internet_data = df_internet_melted[df_internet_melted['Count'] >= slider_value_bar]
if selected_status_bar != 'All':
    filtered_internet_data = filtered_internet_data[filtered_internet_data['Internet Availability'] == selected_status_bar]

# Create the bar chart with filtered data
fig_bar = px.bar(filtered_internet_data, x='refArea_clean', y='Count', color='Internet Availability',
                 title='Internet Availability by Reference Area',
                 labels={'refArea_clean': 'Reference Area', 'Count': 'Count of Availability'},
                 barmode='group')

# Rotate x labels for better readability
fig_bar.update_layout(xaxis_tickangle=-45)

# Show the Bar Chart in Streamlit
st.plotly_chart(fig_bar)

# ------------------ Phone Network Status Sankey Diagram ------------------

# Create a list of unique reference areas and phone network statuses
statuses = ['State of phone network - good', 'State of phone network - acceptable', 'State of phone network - bad']
df_phone_status = df.melt(id_vars=['refArea_clean'], value_vars=statuses, var_name='Phone Network Status', value_name='Count')

# Interactive Features for Sankey Diagram
st.title("Interactive Phone Network Status Visualization")

# Slider for Sankey Diagram
min_count_sankey = int(df_phone_status['Count'].min())
max_count_sankey = int(df_phone_status['Count'].max())
slider_value_sankey = st.slider("Select a minimum count value for Phone Network Status", 
                                min_value=min_count_sankey, 
                                max_value=max_count_sankey, 
                                value=min_count_sankey)

# Dropdown for Sankey Diagram
selected_status_sankey = st.selectbox("Select Phone Network Status to filter", 
                                      options=['All'] + statuses)

# Filter the data for Sankey Diagram
filtered_phone_status_data = df_phone_status[df_phone_status['Count'] >= slider_value_sankey]
if selected_status_sankey != 'All':
    filtered_phone_status_data = filtered_phone_status_data[filtered_phone_status_data['Phone Network Status'] == selected_status_sankey]

# Create the Sankey diagram with filtered data
sources, targets, values = [], [], []
for status in statuses:
    for refArea in filtered_phone_status_data['refArea_clean'].unique():
        count = filtered_phone_status_data[(filtered_phone_status_data['refArea_clean'] == refArea) &
                                           (filtered_phone_status_data['Phone Network Status'] == status)]['Count'].sum()
        if count > 0:
            sources.append(statuses.index(status))
            targets.append(len(statuses) + list(filtered_phone_status_data['refArea_clean'].unique()).index(refArea))
            values.append(count)

# Create Sankey diagram
labels = statuses + list(filtered_phone_status_data['refArea_clean'].unique())
fig_sankey = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
))

# Update layout for readability
fig_sankey.update_layout(title_text="Sankey Diagram of Phone Network Status by Reference Area", font_size=10)

# Show the Sankey Diagram in Streamlit
st.plotly_chart(fig_sankey)