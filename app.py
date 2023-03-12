import time
from pandas import unique
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy import SpotifyOAuth
from secrets_1 import clientSecret,clientID

app = Flask(__name__)
app.secret_key = "BLs029sjO1"
app.config['SESSION_COOKIE_NAME'] = 'Session Cookie 1'
TOKEN_INFO = "token_info"


@app.route('/')
def login():
    sp = spotify_oauth()
    auth_url = sp.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectUser():
    sp = spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('genres', _external=True))


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"

    sp = spotify_oauth()
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60

    if is_expired:
        token_info = sp.refresh_access_token(token_info['refresh_token'])
        session[TOKEN_INFO] = token_info

    return token_info


@app.route('/genres')
def genres():
    try:
        token_info = get_token()
    except:
        print("Please login")
        return redirect("/")

    sp_launch = spotipy.Spotify(auth=token_info['access_token'])
    i = 0
    genre_list = []
    track_genre_list = []

    # loops through your last 30 liked songs and gets the genres of each
    while i < 30:
        track = sp_launch.current_user_saved_tracks(limit=50, offset=0)['items'][i]
        artist = sp_launch.artist(track['track']['album']["artists"][0]["external_urls"]["spotify"])
        genre_list += artist['genres']
        i += 1
        track_genre_list.append([track['track']['id'], artist['genres']])

    # remove duplicates in list
    updatedGenreList = unique(genre_list).tolist()

    for index, genre in enumerate(updatedGenreList):
        print(f"{index + 1}- {genre}")

    # gets the genre that the user wants
    genre_index = input("What genre should your new playlist be? ")
    try:
        user_genre_index = int(genre_index)
        if user_genre_index <= len(updatedGenreList) and user_genre_index > 0:
            print("noted")
        else:
            print("Invalid input. Please enter a valid index.")
    except ValueError:
        print("Invalid input. Please enter a valid index.")
    seed_genre = updatedGenreList[user_genre_index - 1]
    

    def find_match(seed):  
        temporary_list = []
        i = 0
        while i in range(len(track_genre_list)):
            temporary_list += track_genre_list[i][1]  # creating new list from 2d array
            i += 1
            j = 0  # resetting j to zero
            while j in range(len(temporary_list)):
                if temporary_list[j] == seed:  # searching list for the genre
                    return temporary_list
                j += 1
            temporary_list.clear()  # clearing list for next entry (only one entry at a time)
        return 'could not find match'

    # takes in search_2 and returns the corresponding id
    def find_id(list):  
        i = 0
        while i in range(len(track_genre_list)):
            if list == track_genre_list[i][1]:
                return track_genre_list[i][0]
            else:
                i += 1
        return 'could not find match'

    search_2 = find_match(seed_genre)
    track_id = find_id(search_2)
    formatted_id = ['spotify:track:' + track_id]
    print("Found Match")


    # Use the seed track to get 10 recommended tracks
    recommendations = sp_launch.recommendations(seed_tracks=formatted_id, limit=10)
    recommended_tracks = recommendations['tracks']
    print("Got Reccomendations")

    # Create a new playlist with user input as name
    playlist_name = input("What is the name of your new playlist?\n")
    playlist_description = input("What is the description of your new playlist?\n")
    playlist = sp_launch.user_playlist_create(user=sp_launch.current_user()['id'], name=playlist_name, public=False, description=playlist_description)
    print("Created Playlist")
    
    playlist_id = playlist['id']
    
    #add recommended tracks to new playlist 
    def addTracksToPlaylist(sp, recommended_tracks, playlist_id):
        track_ids = [track['id'] for track in recommended_tracks]
        sp.user_playlist_add_tracks(sp.current_user()['id'], playlist_id, track_ids)
        playlist_url = sp.user_playlist(sp.current_user()['id'], playlist_id)['external_urls']['spotify']
        return f"Tracks added to playlist {playlist_url} successfully!"

    return addTracksToPlaylist(sp_launch, recommended_tracks, playlist_id)


# Spotify object
def spotify_oauth():
    return SpotifyOAuth(
        client_id=clientID,
        client_secret=clientSecret,
        redirect_uri=url_for('redirectUser', _external=True),
        scope='user-library-read user-top-read playlist-modify-private ')

if __name__ == '__main__':
    app.run()

