import streamlit as st
import pandas as pd

st.set_page_config(page_title="Safety Stock",
                   page_icon=":chart_with_upwards_trend:")
st.title("Sample Analysis")

st.write("## Upload a Dataset")
url = st.file_uploader("")

if url:
  dff = pd.read_csv(url)
  st.write(dff)

  cols = st.multiselect("Select Columns to Remove", dff.columns)
  dff = dff.drop(cols, axis=1)

  product = st.selectbox("Select the product", dff['Product ID'].unique())
  if product:
    dff = dff[dff["Product ID"] == product].reset_index(drop=True)

  st.header("Aggregating Data")
  agg = st.selectbox("Select Aggregatation Type", ['month', 'year'])

  if agg == 'month':
    dff.Date = pd.to_datetime(dff.Date)
    dff.index = dff.Date

    updated_df = dff.groupby(pd.Grouper(key='Date', freq="M",
                                        axis=0)).sum().reset_index()
    updated_df.index = updated_df['Date']
    updated_df = updated_df.drop(['Date'], axis=1)
    updated_df.index = updated_df.index.date

  if agg == 'year':
    dff.Date = pd.to_datetime(dff.Date)
    dff.index = dff.Date

    updated_df = dff.groupby(pd.Grouper(key='Date', freq="Y",
                                        axis=0)).sum().reset_index()
    updated_df.index = updated_df['Date']
    updated_df = updated_df.drop(['Date'], axis=1)
    updated_df.index = updated_df.index.date

if st.button("Updated DF"):
  st.write(updated_df)
