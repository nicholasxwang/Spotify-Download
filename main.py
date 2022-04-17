import os
from os import system, name
import spotipy
import spotipy.oauth2 as oauth2
import youtube_dl
from youtube_search import YoutubeSearch
import glob
import os
import time
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3
import urllib.request
def clear_terminal():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

client_id = "846095b9ce934b0da3e0aaf3adbf600c"
client_secret = "1d79c77cee124d8f8e20b16f720d65e8"
playlist = input("Input spotify URL: ")
username = "kkbp42dkp4hweuogt99r8t8wf"
#5AbjzbPFE7rMP2ndFqd6mT?si=608373e66f0c4573
playlist_uri = playlist.strip("https://open.spotify.com/playlist/")
if "?" in playlist_uri:
    playlist_uri = playlist_uri[0:playlist_uri.index("?")]
auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)
results = spotify.user_playlist(username, playlist_uri, fields='tracks,next,name')
playlist_name = results['name']
text_file = "songs.txt"
print(u'Writing {0} tracks to {1}.'.format(results['tracks']['total'], text_file))
tracks = results['tracks']
count = -1
for item in tracks['items']:
    os.system("youtube-dl --rm-cache-dir")
    count +=1
    if 'track' in item:
        track = item['track']
    else:
        track = item
    try:
        track_url = track['external_urls']['spotify']
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        track_image = track["album"]["images"][0]["url"]
        track_album = track["album"]["name"]
        print(track_name)
        text_to_search = track_artist + " - " + track_name
        best_url = None
        TOTAL_ATTEMPTS = 100
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
            #'outtmpl' : './songs.',
            # 'outtmpl': './songs.',
            #'outtmpl': './songs',
            'outtmpl': './songs/'+track_artist.replace("/", "_").replace(".", "_").replace("~", "_")+" - "+track_name.replace("/", "_").replace(".", "_").replace("~", "_")+".",
            'keevideo': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([best_url])
            except Exception as e:
                print("Error: " + str(e))



        list_of_files = glob.glob('./songs/*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        if latest_file.split(".")[-1].lower() != "mp3":

            time.sleep(5)
            list_of_files = glob.glob('./songs/*')  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)


            ending = latest_file.split(".")[-1].lower()
            if ending == "part" or ending == "ds_store" or ending == "txt":
                print('MP3 Skipped')
            else:
                print("Making " + latest_file)
                audio = AudioSegment.from_file(latest_file, format=ending)
                audio.export(latest_file.replace(ending, "mp3"), format="mp3")
                os.remove(latest_file)
            latest_file = latest_file.replace(ending, "mp3")


        urllib.request.urlretrieve(track_image, "image.jpg")

        audio = MP3(f"{latest_file}", ID3=ID3)

        # add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except error:
            pass
        open("image.jpg", 'rb').read()
        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=open("image.jpg", 'rb').read()
            )
        )
        audio.save()
        audio = EasyID3(f"{latest_file}")
        audio['title'] = track_name
        audio['artist'] = track_artist
        audio['album'] = track_album
        audio['composer'] = u""  # clear
        audio.save()
        os.remove("image.jpg")

    except KeyError:
        print(u'Skipping track {0} by {1} (local only?)'.format(
            track['name'], track['artists'][0]['name']))
#print(tracks)