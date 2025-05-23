import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Storage Items", layout="wide")

# Connect to database
conn = sqlite3.connect("shelf_books.db")
df = pd.read_sql_query("SELECT * FROM books", conn)

# === 🔎 Barcode search ===
search = st.sidebar.text_input("🔎 Search barcode (full or partial)")

# If searching, skip filters and show matching records
if search:
    results = df[df['barcode'].str.contains(search, case=False, na=False)].sort_values(by='barcode')
    st.title(f"Search Results for '{search}'")
    st.dataframe(results[['barcode', 'floor', 'range', 'ladder', 'shelf', 'position']], use_container_width=True)
    st.stop()

# === 🧭 Filters if not searching ===
st.sidebar.header("📚 Filter by Location")
floor = st.sidebar.selectbox("Floor", sorted(df['floor'].unique()))
range_ = st.sidebar.selectbox("Range", sorted(df['range'].unique()))
ladder = st.sidebar.selectbox("Ladder", sorted(df['ladder'].unique()))
shelf = st.sidebar.selectbox("Shelf", sorted(df['shelf'].unique()))

# Filter results
filtered_df = df[
    (df['floor'] == floor) &
    (df['range'] == range_) &
    (df['ladder'] == ladder) &
    (df['shelf'] == shelf)
].sort_values(by='position')

# Display filtered shelf
st.title(f"Shelf Viewer: Range {range_} - Ladder {ladder} - Shelf {shelf}")
st.dataframe(filtered_df[['position', 'barcode']], use_container_width=True)
