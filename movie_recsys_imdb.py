import pandas as pd
import numpy as np
import streamlit as st

#Load Dataset
data = pd.read_csv("imdb_top_1000.csv")
df = pd.DataFrame(data)
# print(df.head())

#information dataset
# print(df.info())

#feature selection
df = df[["Series_Title", "Released_Year", "Genre", "IMDB_Rating", "Director"]]
# print(df.head())
# print(df.info())

#check missing value
# print(df.isnull().sum())

# #check duplicate data
# print(df.duplicated().sum())

all_genre = set()
for genres in df["Genre"]:
    all_genre.update(genres.split(", "))

all_genre = sorted(list(all_genre))
print(all_genre)

def genre_to_vector(genre, all_genre):
    vector = []
    for g in all_genre:
        if g in genre:
            vector.append(1)
        else:
            vector.append(0)
    return np.array(vector)
df["vector"] = df["Genre"].apply(lambda g: genre_to_vector(g, all_genre))
print(df)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

def recommend_movies(movie_title, df):
    if movie_title not in df["Series_Title"].values:
        return "Film tidak ditemukan dalam database."
    
    idx = df[df["Series_Title"] == movie_title].index[0]
    target_vector = df.loc[idx, "vector"]
    
    # Hitung kesamaan dengan semua film lain
    similarities = []
    for i, row in df.iterrows():
        if i != idx: 
            sim_score = cosine_similarity(target_vector, row["vector"])
            similarities.append((row["Series_Title"],sim_score,row["Genre"]))
        
    filtered_similarities = [] 

    for sim in sorted(similarities, key=lambda x: x[1], reverse=True):
        # print(sim)
        if sim[1] > 0: 
            filtered_similarities.append(sim)

    # Urutkan berdasarkan nilai similarity tertinggi
    filtered_similarities = sorted(filtered_similarities, key=lambda x: x[1], reverse=True)

    return [(title, genre) for title, _, genre in filtered_similarities[:6]]



# if __name__ == "__main__":
#     movie_title = input("Type movie title you like: ")
#     rec_movies = recommend_movies(movie_title, df)
#     print(f"Movie recommendation for {movie_title} :")
#     for movie in rec_movies:
#         print(movie)


# Streamlit UI
st.title("🎬 Sistem Rekomendasi Film")
st.write("Masukkan judul film yang kamu suka, dan dapatkan rekomendasi berdasarkan genre!")

movie_title = st.text_input("Masukkan judul film:")
if st.button("Dapatkan Rekomendasi"):
    if movie_title:
        rec_movies = recommend_movies(movie_title, df)
        if isinstance(rec_movies, str):
            st.error(rec_movies)
        else:
            st.subheader("Rekomendasi Film:")
            for i, (movie, genre) in enumerate(rec_movies, start=1):
                st.markdown(f"{i}. **{movie}** <span style='color:green'>({genre})</span>", unsafe_allow_html=True)

    else:
        st.warning("Harap masukkan judul film!")

