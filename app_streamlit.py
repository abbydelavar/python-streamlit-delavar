"""
This app creates a Streamlit dashboard that looks at how students performed on
tests and correlation to certain demographical factors.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# This adds a page title to the html and makes the plots full width
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Read in the csv used for the dashboard and melt the data to use for histogram
df = pd.read_csv("StudentsPerformance.csv")
vars_to_melt = ["Math Score", "Reading Score", "Writing Score", "Average Score"]
histogram_data_df = pd.melt(
    df,
    id_vars=df.columns.difference(vars_to_melt),
    value_vars=vars_to_melt,
    var_name="Subject Score",
    value_name="Test Score (out of 100)",
)

# This fixes the large amount of whitespace that Streamlit has by default
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)

# Create title for web page
st.title(
    "High School Student Test Performance With Correlated Demographic Data",
)
st.write("Dataset provided by http://roycekimmons.com/tools/generated_data/exams")
# Create slider that gets the First and Third quartile as the initial
# values
values = st.slider(
    "Select a range of test score values",
    0,
    100,
    (
        int(np.percentile(df["Average Score"], 25)),
        int(np.percentile(df["Average Score"], 75)),
    ),
    step=1,
)

# Filter the data based on what the user selects for the slider
data_for_plots = histogram_data_df.loc[
    histogram_data_df["Test Score (out of 100)"].between(values[0], values[1]), :
].copy()

# Create histogram based on type of score and the score that they got
fig = px.histogram(
    data_for_plots,
    x="Test Score (out of 100)",
    color="Subject Score",
    text_auto=True,
)
fig.update_layout(height=300, yaxis_title="Count of Students")
st.plotly_chart(fig, use_container_width=True, height=300)

# Create three columns for each of the pie charts to be shown
col1, col2, col3 = st.columns(3)

# Create column one with ethnicity pie chart
with col1:
    st.write(f"Ethnicity in Score Range ({values[0]}, {values[1]})")
    pie_fig = px.pie(data_for_plots.sort_values("Ethnicity"), names="Ethnicity")
    pie_fig.update_layout(height=300)
    st.plotly_chart(pie_fig, use_container_width=True, height=300)

# Create column two with parental level of education pie chart
with col2:
    st.write(f"Parental Level of Education in Score Range ({values[0]}, {values[1]})")
    pie_fig = px.pie(
        data_for_plots.sort_values("Parental Level of Education"),
        names="Parental Level of Education",
    )
    pie_fig.update_layout(height=300)
    st.plotly_chart(pie_fig, use_container_width=True, height=300)

# Create column three with gender pie chart
with col3:
    st.write(f"Gender in Score Range ({values[0]}, {values[1]})")
    pie_fig = px.pie(data_for_plots.sort_values("Gender"), names="Gender")
    pie_fig.update_layout(height=300)
    st.plotly_chart(pie_fig, use_container_width=True, height=300)
