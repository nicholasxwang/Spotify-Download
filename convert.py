folder = "./Pop Music (Winter 2021)"
from os import walk
# from pydub import AudioSegment
#
f = []
for (dirpath, dirnames, filenames) in walk(folder):
    f.extend(filenames)
    break
endings = {}
for i in f:
    splitted = i.split(".")
    try:
        endings[splitted[-1].lower()]+=1
    except:
        endings[splitted[-1].lower()] = 1
print(endings)
# for i in endings.keys():
#     print(f"{i} ({endings[i]})")
# for i in f:
#     print(f"[{i}]")
#     file = i
#     ending = i.split(".")[-1].lower()
#     if ending == "m4a":
#         print("- Starting Conversion [m4a]")
#         print("- File: ./Pop Music (Winter 2021)/"+i)
#         print("- Export: "+"./mp3_export/"+i.replace(ending, "mp3"))
#         song = AudioSegment.from_file("./Pop Music (Winter 2021)/"+i, format=ending)
#         print("- Fetched Audio Segment")
#         song.export("./mp3_export/"+i.replace(ending, "mp3"), format="mp3")
#
#     if ending == "webm":
#         print("- Starting Conversion [webm]")
#         print("- File: ./Pop Music (Winter 2021)/" + i)
#         print("- Export: " + "./mp3_export/" + i.replace(ending, "mp3"))
#         song = AudioSegment.from_file("./Pop Music (Winter 2021)/" + i, format=ending)
#         print("- Fetched Audio Segment")
#         song.export("./mp3_export/" + i.replace(ending, "mp3"), format="mp3")
#     if ending == "part":
#         print("- Cannot convert this file!")
#     if ending == "txt" or ending == "ds_store":
#         print(f"- We are skipping files with the ending {ending}")

# import convertapi
#
# convertapi.api_secret = '890103485'
# for i in f:
#     print(f"[{i}]")
#     file = i
#     ending = i.split(".")[-1].lower()
#     if ending == "m4a":
#         print("- Starting Conversion [m4a]")
#         result = convertapi.convert('mp3', {'File': "./Pop Music (Winter 2021)/"+i})
#         print("- Saving the file...")
#         result.file.save("./mp3_export/"+i.replace(ending, "mp3"))
#
#     if ending == "webm":
#         print("- Starting Conversion [m4a]")
#         result = convertapi.convert('mp3', {'File': "./Pop Music (Winter 2021)/" + i})
#         print("- Saving the file...")
#         result.file.save("./mp3_export/" + i.replace(ending, "mp3"))
#     if ending == "part":
#         print("- Cannot convert this file!")
#     if ending == "txt" or ending == "ds_store":
#         print(f"- We are skipping files with the ending {ending}")

from pydub import AudioSegment
for i in f:
    #https://github.com/jiaaro/pydub/issues/450
    #brew uninstall ffmpeg
    #brew install ffmpeg
    ending = i.split(".")[-1].lower()
    if ending == "part" or ending == "ds_store" or ending == "txt":
        continue
    print("Making "+i)
    audio = AudioSegment.from_file("./Pop Music (Winter 2021)/"+i, format=ending)
    audio.export("./MP3-Music/"+i.replace(ending,"mp3"), format="mp3")