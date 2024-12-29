from moviepy import *
import requests
from mutagen.mp3 import MP3
import uuid

# step 1 define params
fromVerse = 1
toVerse = 2
suranNumber = 4
reciter = 7 # Max 11 visit https://api.quran.com/api/v4/resources/recitations to see all reciters

# for each verse, display the verse, play the audio
# each text clip should have the duration of its audio clip

total_duration = 0;
txt_clips = []
audio_clips = []

for i in range(fromVerse, toVerse):
    
    ayahKey = f"{suranNumber}:{i}"
    verse = requests.get(f"https://api.quran.com/api/v4/recitations/{reciter}/by_ayah/{ayahKey}").json()
    audio_link = "https://verses.quran.com/"+verse["audio_files"][0]["url"]
   
    text = requests.get(f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={ayahKey}").json()["verses"][0]["text_uthmani"]
    
    # text = text + " " + convert_to_arabic(i);

    # convert number to arabic

    # save the file, create the clip and duration
    response = requests.get(audio_link)
    
    fileName = f"./tmp_workspace/{uuid.uuid4()}.mp3"
    with open(fileName, "wb") as file:
        file.write(response.content)
    
    audioFileLength = MP3(fileName).info.length
    
    total_duration = total_duration + audioFileLength;
    
    # create the text clip
    
    txt_clip = TextClip(
        font="./AlQalamQuran.ttf",
        method='caption',
        # font="./font.ttf",
        text=text,
        size=(600, 600),
        text_align='center',
        font_size=40,
        color='white',
        bg_color='black',
        ).with_duration(audioFileLength).with_position('center')

    txt_clip.audio = AudioFileClip(fileName)
    
    txt_clips.append(txt_clip)
#
clip = (
    VideoFileClip("./clip.mp4")
    .with_volume_scaled(1)
)

clip = vfx.Loop(duration=total_duration + 1).apply(clip)

concat_txt_clips = concatenate_videoclips(txt_clips).with_position('center')

final_video = CompositeVideoClip([clip, concat_txt_clips])
final_video.write_videofile("result.mp4")


