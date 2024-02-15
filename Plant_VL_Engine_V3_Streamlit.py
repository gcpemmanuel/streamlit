#!/usr/bin/env python
# coding: utf-8

# In[2]:


import plotly.graph_objects as go
import random
import pandas as pd
from collections import OrderedDict
import plotly.colors
import streamlit as st

# set the title of the app
st.title('CSV File Upload and Plotting')

# add a file uploader widget
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')

# if a file is uploaded
if uploaded_file is not None:
    # read the file into a pandas dataframe
    data_o = pd.read_csv(uploaded_file)
    
    if not data_o.empty:
    
        # Create a multiselect widget for users to specify the column order
        column_order = st.multiselect('Select the column order', data_o.columns.tolist(), default=data_o.columns.tolist())

        # Create a new DataFrame with the columns in the specified order
        data_o = data_o[column_order]

        # Create a select box for the first-level filter
        selected_categories = st.multiselect('Select categories of first column', data_o[data_o.columns[0]].unique())

        # Filter the dataframe based on the selected category
        data = data_o[data_o[data_o.columns[0]].isin(selected_categories)]

        # Add a text input widget for the second-level filter
        second_level_filter = st.text_input('Filter by text (contains) on second column', '')

        # Apply the second-level filter to the filtered data
        if second_level_filter:
            data = data[data[data.columns[1]].str.contains(second_level_filter, case=False, na=False)]

        # display the dataframe
        st.write('Dataframe:')
        st.write(data)

        # Creat the source Dictionary from level_1_2, level_2_3, level_3_4 etc
        levels_s={}
        for j in range(len(data.columns)):
            if j+2 <= len(data.columns):
                level_s = 'level_' + str(j+1) + '_' + str(j+2)
                levels_s[level_s] = []
                for i in list(data[data.columns[j]].unique()):
                    levels_s[level_s].extend([i] * len(data[data[data.columns[j]]==i][data.columns[j+1]].unique()))


        # Creat the target Dictionary from level_2_1, level_3_2, level_4_3 etc
        levels_t={}
        for j in range(len(data.columns)):
            if j+2 <= len(data.columns):
                level_t = 'level_' + str(j+2) + '_' + str(j+1)
                levels_t[level_t] = []
                for i in list(data[data.columns[j]].unique()):
                    levels_t[level_t].extend(list(data[data[data.columns[j]]==i][data.columns[j+1]].unique()))


        # Extract the source and target values into a list from the source and target dictionary
        source_name = [value for sublist in levels_s.values() for value in sublist]
        target_name = [value for sublist in levels_t.values() for value in sublist]


        # Create unique node number for every unique value in the dataset
        node_nam = list(OrderedDict.fromkeys(source_name+target_name))
        node_num = [i for i in range(len(node_nam))]
        node_number = dict(zip(node_nam,node_num))

        # Extact the node numbers into a list from source list
        source = []
        for i in source_name:
            source.append(node_number[i])

        # Extact the node numbers into a list from target list
        target = []
        for i in target_name:
            target.append(node_number[i])

        # Calculate the number of flows between the nodes
        flow = 0
        for i in range(len(data.columns)):
            if i+1 < len(data.columns):
                for j in data[data.columns[i]].unique():
                    flow = flow + len(data[data[data.columns[i]]==j][data.columns[i+1]].unique())

        # color sequence in a list
        mild_color_palette = plotly.colors.qualitative.Antique + plotly.colors.qualitative.Pastel



        # create Sankey diagram

        value = [1 for i in range(flow)]
        colors = mild_color_palette
        # create the nodes for the chartlightgray
        nodes = dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_nam,
        )

        # create the links between the nodes
        links = dict(
            source=source,
            target=target,
            value=value,
            color=[colors[i] for i in source]
        )

        # create the Sankey diagram figure
        fig = go.Figure(data=[go.Sankey(node=nodes, link=links)])

        # update the figure layout
        fig.update_layout(
            title_text="Sankey Plot",
            font=dict(size=12, color="grey"),
            width = 900,
            height = 500,
            paper_bgcolor='rgb(245, 245, 245)',
            clickmode='event'
        )

        # display the figure
        st.write(f'<style>.sankeylabel'+'{fill: rgba(0, 0, 0, 1) !important;}</style>', unsafe_allow_html=True)
        st.plotly_chart(fig)

        # Apply custom JavaScript to change label font color
        st.write(
            """
            <script>
            const labels = document.querySelectorAll('.sankeylabel');
            labels.forEach(label => label.style.fill = 'black');
            </script>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write('Select the valid columns')
    

