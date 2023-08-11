import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

df = pd.read_csv("StudentsPerformance.csv")
vars_to_melt = ["Math Score", "Reading Score", "Writing Score", "Average Score"]
histogram_data_df = pd.melt(
    df,
    id_vars=df.columns.difference(vars_to_melt),
    value_vars=vars_to_melt,
    var_name="Type of Score",
    value_name="Score",
)
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
st.title("Student Performance")

# Plot!
values = st.slider(
    "Select a range of values",
    0,
    100,
    (
        int(np.percentile(df["Average Score"], 25)),
        int(np.percentile(df["Average Score"], 75)),
    ),
    step=1,
)

data_for_plots = histogram_data_df.loc[
    histogram_data_df["Score"].between(values[0], values[1]), :
].copy()

# Create histogram based on type of score and the score that they got
fig = px.histogram(
    data_for_plots,
    x="Score",
    color="Type of Score",
    text_auto=True,
)
fig.update_layout(height=300)

st.plotly_chart(fig, use_container_width=True, height=300)

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"Ethnicity in Score Range ({values[0]}, {values[1]})")
    pie_fig = px.pie(data_for_plots.sort_values("Ethnicity"), names="Ethnicity")
    pie_fig.update_layout(height=300)
    st.plotly_chart(pie_fig, use_container_width=True, height=300)

with col2:
    st.write(f"Parental Level of Education in Score Range ({values[0]}, {values[1]})")
    pie_fig = px.pie(
        data_for_plots.sort_values("Parental Level of Education"),
        names="Parental Level of Education",
    )
    pie_fig.update_layout(height=300)
    st.plotly_chart(pie_fig, use_container_width=True, height=300)

with col3:
    st.write(f"Gender in Score Range ({values[0]}, {values[1]})")
    pie_fig = px.pie(data_for_plots.sort_values("Gender"), names="Gender")
    pie_fig.update_layout(height=300)
    st.plotly_chart(pie_fig, use_container_width=True, height=300)
