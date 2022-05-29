
import streamlit as st
import pickle
import pandas as pd
import requests

with st.sidebar:
    st.title('Helpful Links')
    st.write('More info')
    st.markdown("[IMDB](https://www.imdb.com/)")
    # st.markdown("[TMDB](https://www.themoviedb.org/)")
    st.markdown("[ROTTEN TOMATOES](https://www.rottentomatoes.com/)")
    st.write('watch it on')
    st.markdown("[NETFLIX](https://www.netflix.com/in/)")
    st.markdown("[HOTSTAR](https://www.hotstar.com/in)")
    st.markdown("[AMAZON PRIME](https://www.primevideo.com/)")
    

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=e8dcddd43d2d1f9aef812dc7c6992d68&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=e8dcddd43d2d1f9aef812dc7c6992d68&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    tagline = data['tagline']
    overview = data['overview']
    date = data['release_date']
    rating = data['vote_average']
    link = data['homepage']
    gen = data['genres']
    genre = []
    x = 0
    for i in gen:
        genre.append(data['genres'][x]['name'])
        x = x+1
    # st.snow()
    
    return tagline,overview,date,rating,link,genre


def search(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[0:1]

    tagline = '-1'
    movie_overview = '0'
    
    date = '2'
    rating = '3'
    link = '4'
    getmovie = []
    movie_poster = []
    genre = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        getmovie.append(movies.iloc[i[0]].title)
        movie_poster.append(fetch_poster(movie_id))
        tagline,movie_overview,date,rating,link,genre = (fetch_details(movie_id))
            
    return getmovie,movie_poster,tagline,movie_overview,date,rating,link,genre

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies_list = movies_list['titles']
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('REC Top-5')
dropdown =[]
for i in movies['title'].values:
    dropdown.append(i)
selected_movie_name = st.selectbox('Search Here!!',['select'] + dropdown)
        

# st.button('Find')
if selected_movie_name == 'select':
    st.write("No movie selected")
else:
    name,poster,tagline,overview,date,rating,linky,genre = search(selected_movie_name)
    
    st.header(name[0])
    col1, col2 = st.columns(2)
    with col1:
        st.image(poster[0])
    with col2:   
        st.caption(tagline)
        st.text(' ')
        st.text('About')
        st.write    (overview)
        st.text(' ')
        st.selectbox('See Genre',genre)
        st.write('Release Date(yyyy-mm-dd) - ',date)
        st.write('Ratings - ',rating)
        st.markdown(f"LINK - [{name[0]}]({linky})")
    st.text("Checkout Recommendations")
    if st.button('Recommend'):
        names,posters = recommend(selected_movie_name)

        col1, col2, col3, col4,col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        
            
        with col2:
            st.text(names[1])
            st.image(posters[1])
                    
            
        with col3:
            st.text(names[2])
            st.image(posters[2])


        with col4:
            st.text(names[3])
            st.image(posters[3])

            
        with col5:
            st.text(names[4])
            st.image(posters[4])
