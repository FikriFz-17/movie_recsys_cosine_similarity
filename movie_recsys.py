import pandas as pd
import numpy as np

data = {
    "movie_id": [1, 2, 3, 4, 5, 6],
    "title": [
        "The Matrix",
        "Inception",
        "Interstellar",
        "The Social Network",
        "The Godfather",
        "Dr Stone"
    ],
    "genre": [
        "Sci-Fi, Action",
        "Sci-Fi, Thriller",
        "Sci-Fi, Drama",
        "Biography, Drama",
        "Crime, Drama",
        "Sci-Fi, Fantasy"

    ]
}

df = pd.DataFrame(data)
print("Movie Data : ")
print(df, "\n")

all_genre = set()
for genres in df["genre"]:
    all_genre.update(genres.split(", "))

all_genre = sorted(list(all_genre))
# print(all_genre)

def genre_to_vector(genre, all_genre):
    vector = []
    for g in all_genre:
        if g in genre:
            vector.append(1)
        else:
            vector.append(0)
    return np.array(vector)

df["vector"] = df["genre"].apply(lambda g: genre_to_vector(g, all_genre))
# print(df)

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

def recommend_movies(movie_title, df):
    if movie_title not in df["title"].values:
        return "Film tidak ditemukan dalam database."
    
    idx = df[df["title"] == movie_title].index[0]
    target_vector = df.loc[idx, "vector"]
    
    # Hitung kesamaan dengan semua film lain
    similarities = []
    for i, row in df.iterrows():
        if i != idx: 
            sim_score = cosine_similarity(target_vector, row["vector"])
            similarities.append((row["title"], sim_score))
        
    filtered_similarities = [] 

    for sim in similarities:
        # Tampilkan nilai similarity
        print(sim)
        if sim[1] > 0: 
            filtered_similarities.append(sim)

    # Urutkan berdasarkan nilai similarity tertinggi
    filtered_similarities = sorted(filtered_similarities, key=lambda x: x[1], reverse=True)

    return [title for title, _ in filtered_similarities[:]]


if __name__ == "__main__":
    movie_title = input("Type movie title you like: ")
    rec_movies = recommend_movies(movie_title, df)
    print(f"Movie recommendation for {movie_title} :")
    for movie in rec_movies:
        print(movie)
