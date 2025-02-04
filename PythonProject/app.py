from flask import Flask, render_template, request
import pickle
import requests
import pandas as pd



app = Flask(__name__)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def fetch_trailer(movie_id):
    api_key = "989d4f230a926adab27e6b2c26bddbc4"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US&api_key={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        return "Ошибка запроса к API"

    data = response.json()
    
    if "results" not in data or len(data["results"]) == 0:
        return "Трейлер не найден"

    # Ищем трейлер (обычно это 'Trailer' и 'YouTube')
    for video in data["results"]:
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"

    return "Трейлер не найден"

    



movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_info = pickle.load(open("movies_info.pkl", 'rb'))
movies_list = movies['title'].values

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    recommend_vote_avarage = []
    recommend_origina_language = []
    recommend_overwiev = []
    recommend_genres = []
    recomend_date = []
    recommend_vote_count = []
    recomend_trailers = []
    
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_vote_avarage.append(movies_info.iloc[i[0]].vote_average)
        recommend_poster.append(fetch_poster(movies_id))
        recommend_origina_language.append(movies_info.iloc[i[0]].original_language)
        recommend_overwiev.append(movies_info.iloc[i[0]].overview)
        recommend_genres.append(movies_info.iloc[i[0]].genre)
        recomend_date.append(movies_info.iloc[i[0]].release_date)
        recommend_vote_count.append(movies_info.iloc[i[0]].vote_count)
        recomend_trailers.append(fetch_trailer(movies_id))
    
    return recommend_movie, recommend_poster, recommend_vote_avarage, recommend_origina_language, recommend_overwiev, recommend_genres, recomend_date, recommend_vote_count, recomend_trailers


@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/find')
# def findHhome():
#     return render_template("find.html")


@app.route('/find', methods = ["GET", "POST"])
def find():
    recommended_movies = []
    recommended_posters = []
    recommend_vote_avarages = []
    recommend_original_languages = []
    recommend_overviews = []
    recommend_genres = []
    recommend_dates = []
    recommend_vote_counts = []
    recommend_trailers = []

    selected_movie = None
    selected_poster = None
    selected_avarage = None
    selected_origina_language = None
    selected_overwiev = None
    selected_genres = None
    selected_date = None
    selected_vote_count = None
    selected_trailer = None

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        
        index = movies[movies['title'] == selected_movie].index[0]
        movies_id = movies.iloc[index].id
        
        selected_poster = fetch_poster(movies_id)
        selected_avarage = movies_info.iloc[index].vote_average
        selected_origina_language = movies_info.iloc[index].original_language
        selected_overwiev = movies_info.iloc[index].overview
        selected_genres = movies_info.iloc[index].genre
        selected_date = movies_info.iloc[index].release_date
        selected_vote_count = movies_info.iloc[index].vote_count
        selected_trailer = fetch_trailer(movies_id)

        

        
        if selected_movie:
            recommended_movies, recommended_posters, recommend_vote_avarages, recommend_original_languages, recommend_overviews, recommend_genres, recommend_dates, recommend_vote_counts, recommend_trailers = recommend(selected_movie)


    return render_template("find.html", 
                           movies_list = movies_list,
                           selected_movie = selected_movie,
                           selected_poster = selected_poster,
                           selected_avarage = selected_avarage,
                           selected_origina_language = selected_origina_language,
                           selected_overwiev = selected_overwiev,
                           selected_genres = selected_genres,
                           selected_date = selected_date,
                           selected_vote_count = selected_vote_count,
                           selected_trailer = selected_trailer,
                            
                           recommended_movies = recommended_movies,
                           recommended_posters = recommended_posters,
                           recommend_vote_avarages = recommend_vote_avarages,
                           recommend_original_languages = recommend_original_languages,
                           recommend_overviews = recommend_overviews,
                           recommend_genres = recommend_genres,
                           recommend_dates = recommend_dates,
                           recommend_vote_counts = recommend_vote_counts,
                           recommend_trailers = recommend_trailers,
                           
                           zip = zip)

if __name__ == "__main__":
    app.run(debug=True)