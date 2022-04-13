from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3


audio = MP3("./songs/(여자)아이들((G)I-DLE) - 'TOMBOY' Official Music Video-Jh4QFaPmdss.mp3", ID3=ID3)

# add ID3 tag if it doesn't exist
try:
    audio.add_tags()
except error:
    pass
open('ineverdie.jpeg',  'rb').read()
audio.tags.add(
    APIC(
        encoding=3, # 3 is for utf-8
        mime='image/jpeg', # image/jpeg or image/png
        type=3, # 3 is for the cover image
        desc=u'Cover',
        data=open('ineverdie.jpeg',  'rb').read()
    )
)
audio.save()
audio = EasyID3("./songs/(여자)아이들((G)I-DLE) - 'TOMBOY' Official Music Video-Jh4QFaPmdss.mp3")
audio['title'] = u"TOMBOY"
audio['artist'] = u"(여자)아이들((G)I-DLE)"
audio['album'] = u"I NEVER DIE"
audio['composer'] = u"" # clear
audio.save()