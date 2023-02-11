from flask import Flask, render_template, request
import pickle
import numpy as np, pandas as pd

app = Flask(__name__)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies)

@app.route('/')
def home():
    return render_template('home.html',
                           title = list(movie_list['title'].values),
                           director=list(movie_list['director'].values),
                           votes=list(movie_list['vote_count'].values),
                           rating=list(movie_list['vote_average'].values),
                           overview = list(movie_list['overview'].values),
                           cast = list(movie_list['cast'].values),
                           year = list(movie_list['year'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods = ['post'])
def recommend():
    input = request.form.get('user_input')
    movie_index = movies[movies['title'] == input].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse= True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    for i  in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return render_template('recommend.html', 
                           title = list(movies['title'].values),
                           data= recommended_movies)

if __name__ == "__main__":
    app.run(debug= True)