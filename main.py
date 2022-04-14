import os
from os import system, name
import spotipy
import spotipy.oauth2 as oauth2
import youtube_dl
from youtube_search import YoutubeSearch
def clear_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

client_id = "846095b9ce934b0da3e0aaf3adbf600c"
client_secret = "1d79c77cee124d8f8e20b16f720d65e8"
username = "kkbp42dkp4hweuogt99r8t8wf"
playlist_uri = "6a3BM9U9pm5R4OoXuEyfBa"
auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)
results = spotify.user_playlist(username, playlist_uri, fields='tracks,next,name')
playlist_name = results['name']
text_file = "songs.txt"
print(u'Writing {0} tracks to {1}.'.format(results['tracks']['total'], text_file))
tracks = results['tracks']
for item in tracks['items']:
    if 'track' in item:
        track = item['track']
    else:
        track = item
    try:
        track_url = track['external_urls']['spotify']
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        print(track_name)
        text_to_search = track_artist + " - " + track_name
        best_url = None
        TOTAL_ATTEMPTS = 10
        attempts_left = TOTAL_ATTEMPTS
        while attempts_left > 0:
            try:
                results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
                best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
                break
            except IndexError:
                attempts_left -= 1
                print("No valid URLs found for {}, trying again ({} attempts left).".format(
                    text_to_search, attempts_left))
        if best_url is None:
            print("No valid URLs found for {}, skipping track.".format(text_to_search))
            continue
        # Run you-get to fetch and download the link's audio
        print("Initiating download for {}.".format(text_to_search))
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }

            ],
            #'outtmpl': './songs/'
            # 'outtmpl': 'songs'
            # 'outtmpl': 'songs/'
            # 'outtmpl': '/songs'
            #'outtmpl': '/songs/'
            #'outtmpl' : '~/Users/NicholasWang/spotify-to-mp3-python/songs'
            'outtmpl' : '~/Users/NicholasWang/spotify-to-mp3-python/songs.'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([best_url])
            except Exception as e:
                print("Error: " + str(e))

        import glob
        import os

        list_of_files = glob.glob('./songs')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
    except KeyError:
        print(u'Skipping track {0} by {1} (local only?)'.format(
            track['name'], track['artists'][0]['name']))
#print(tracks)