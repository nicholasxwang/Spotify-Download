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
def add_album_art(file_path, image, title, artist, album):
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, APIC, error
    from mutagen.easyid3 import EasyID3
    import urllib.request
    urllib.request.urlretrieve(image, "image.jpg")

    audio = MP3(f"./songs/{file_path}", ID3=ID3)

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
    audio = EasyID3(f"./songs/{file_path}")
    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio['composer'] = u""  # clear
    audio.save()

def convert_to_mp3(file):
    from pydub import AudioSegment
    ending = file.split(".")[-1].lower()
    if ending == "part" or ending == "ds_store" or ending == "txt":
        print('MP3 Skipped')
    else:
        print("Making " + file)
        audio = AudioSegment.from_file("./songs/" + file, format=ending)
        audio.export("./songs/" + file.replace(ending, "mp3"), format="mp3")

def write_tracks(text_file, tracks):

    # Writes the information of all tracks in the playlist to a text file. 
    # This includins the name, artist, and spotify URL. Each is delimited by a comma.
    text_file = str(text_file)
    tracks = dict(tracks)
    with open(text_file, 'w+', encoding='utf-8') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['external_urls']['spotify']
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    csv_line = track_name + "," + track_artist + "," + track_url + "\n"
                    try:
                        file_out.write(csv_line)
                    except UnicodeEncodeError:  # Most likely caused by non-English song names
                        print("Track named {} failed due to an encoding error. This is \
                            most likely due to this song having a non-English name.".format(track_name))
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username, playlist_id):
    username = str(username)
    playlist_id = str(playlist_id)
    results = spotify.user_playlist(username, playlist_id, fields='tracks,next,name')
    playlist_name = results['name']
    text_file = "songs.txt"
    print(u'Writing {0} tracks to {1}.'.format(results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)
    return playlist_name


def find_and_download_songs(reference_file):
    reference_file = str(reference_file)
    TOTAL_ATTEMPTS = 10
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            clear_terminal()
            temp = line.split(",")
            name, artist = temp[0], temp[1]
            text_to_search = artist + " - " + name
            best_url = None
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
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([best_url])
                except Exception as e:
                    print("Error: "+e)
            #get latest file
            import glob
            import os

            list_of_files = glob.glob('/songs/')  # * means all if need specific format then *.csv
            print(list_of_files)
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)
            convert_to_mp3(latest_file)


# Parameters
client_id = "846095b9ce934b0da3e0aaf3adbf600c"
client_secret = "1d79c77cee124d8f8e20b16f720d65e8"
username = "kkbp42dkp4hweuogt99r8t8wf"
playlist_uri = "6a3BM9U9pm5R4OoXuEyfBa"
auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)
playlist_name = write_playlist(username, playlist_uri)
reference_file = "{}.txt".format("songs")
# Create the playlist folder
if not os.path.exists("songs"):
    os.makedirs("songs")
os.rename(reference_file, "songs" + "/" + reference_file)
os.chdir("songs")
find_and_download_songs(reference_file)
clear_terminal()
print("Converting to MP3...")
convert_to_mp3("songs")
clear_terminal()
print("Operation complete.")
