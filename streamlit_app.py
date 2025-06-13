import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
from wordcloud import WordCloud

df = pd.read_csv('imdb_top_250_movies.csv')
df['rating'] = df['rating'].astype(float)
df['year'] = df['year'].astype(int)
df['has_part'] = df['title'].str.contains(r"(Part|Chapter|Episode|Vol\.|Volume|II|III|IV|V)", flags=re.IGNORECASE, regex=True)


st.set_page_config(page_title="🦠 SQL Me Later - IMDb Dashboard", layout="wide")
st.markdown("""
    <style>
    .css-18e3th9 {
        background-color: #FFC0CB;
    }
    .css-1v3fvcr {
        background-color: #ffccff;
    }
    </style>
""", unsafe_allow_html=True)
st.title("🎬 SQL Me Later - Where Data Meets Drama 🍿")

st.sidebar.header("🌟 Customize the display")
st.sidebar.markdown("**✨ Your Favorite**")

st.sidebar.markdown("""
    <style>
    .css-1v3fvcr {
        background-color: #ff80b3;
    }
    </style>
""", unsafe_allow_html=True)

years = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox("📅 Choose Year", options=["All"] + years)

min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 10.0, 8.0, step=0.1)


part_filter = st.sidebar.radio("🎬 Does the title contain a part?", ["All", "Yes", "No"])


search_text = st.sidebar.text_input("🔍 Search by Movie Title")


filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

if part_filter == "Yes":
    filtered_df = filtered_df[filtered_df['has_part'] == True]
elif part_filter == "No":
    filtered_df = filtered_df[filtered_df['has_part'] == False]

if search_text:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_text, case=False, na=False)]

# Show movies after filtering
st.markdown(f"### 🌸 Showing **{len(filtered_df)}** movies after filtering")

# Sidebar selection for visualizations
option = st.sidebar.selectbox("🎨 Choose Visualization", [
    "📊 Rating Distribution",
    "📅 Number of Movies per Year",
    "🌟 Top 10 Movies",
    "☁️ WordCloud",
    "🎯 Scatterplot",
    "🥧 Movies with Parts"
])


movie_list_container = st.empty()


if option == "📊 Rating Distribution":
    st.markdown("### 📊 IMDb Rating Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df['rating'], bins=20, kde=True, color='hotpink', ax=ax)
    st.pyplot(fig)

elif option == "📅 Number of Movies per Year":
    st.markdown("### 📅 Number of Movies per Year")
    year_counts = filtered_df['year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(x=year_counts.index, y=year_counts.values, color='lightblue', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

elif option == "🌟 Top 10 Movies":
    st.markdown("### 🌟 Top 10 Movies by Rating")
    top_10 = filtered_df.sort_values(by='rating', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='rating', y='title', data=top_10, palette='magma', ax=ax)
    st.pyplot(fig)

elif option == "☁️ WordCloud":
    st.markdown("### ☁️ WordCloud for Movie Titles")
    text = ' '.join(filtered_df['title'])
    wordcloud = WordCloud(width=800, height=400, background_color='lavender', colormap='coolwarm').generate(text)
    st.image(wordcloud.to_array(), use_column_width=True)

elif option == "🎯 Scatterplot":
    st.markdown("### 🎯 Scatterplot: Rating vs Year")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x='year', y='rating', alpha=0.7, hue='rating', palette='coolwarm', ax=ax)
    st.pyplot(fig)

elif option == "🥧 Movies with Parts":
    st.markdown("### 🥧 Percentage of Movies with Parts in Title")
    fig, ax = plt.subplots(figsize=(6, 6))
    filtered_df['has_part'].value_counts().plot.pie(labels=['No Part', 'Has Part'], autopct='%1.1f%%', colors=['lightcoral', 'lightgreen'], ax=ax)
    st.pyplot(fig)


movie_list_container.dataframe(filtered_df[['title', 'year', 'rating']].reset_index(drop=True), use_container_width=True)
