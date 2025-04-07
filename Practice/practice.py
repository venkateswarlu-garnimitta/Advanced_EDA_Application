import streamlit as st
import plotly.express as px
import plotly.io as pio
import pandas as pd
import seaborn as sns

df = sns.load_dataset("iris")
fig = px.scatter(df, x="sepal_length", y="sepal_length", color="species", title="Iris Plot")

# Save a lightweight snapshot of the graph
pio.write_image(fig, "scatter_plot_snapshot.png", format="png", width=800, height=600)

