from moviepy import *
import requests
from mutagen.mp3 import MP3
import uuid

# step 1 define params
fromVerse = 33
toVerse = 42
suranNumber = 80
reciter = 4 # Max 11 visit https://api.quran.com/api/v4/resources/recitations to see all reciters

clip = (
    VideoFileClip("./good_clips/horizontal.mp4")
    .with_volume_scaled(1)
)


# This script is based on a clip that is 720x1280
# To make adjustments create a multiplier
multiplierHeight = clip.h / 1280;
multiplierWidth = clip.w / 720;

# for each verse, display the verse, play the audio
# each text clip should have the duration of its audio clip

total_duration = 0;
txt_clips = []
audio_clips = []
translation_txt_clips = []

for i in range(fromVerse, toVerse + 1):
    
    ayahKey = f"{suranNumber}:{i}"
    verse = requests.get(f"https://api.quran.com/api/v4/recitations/{reciter}/by_ayah/{ayahKey}").json()
    audio_link = "https://verses.quran.com/"+verse["audio_files"][0]["url"]
   
    text =  requests.get(f"https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={ayahKey}").json()["verses"][0]["text_uthmani"]
    translation = requests.get(f"https://api.alquran.cloud/v1/ayah/{ayahKey}/en.hilali").json()["data"]["text"]
    # text =  text + " " + convert_to_arabic(i);

    # convert number to arabic

    # save the file, create the clip and duration
    response = requests.get(audio_link)
    
    fileName = f"./tmp_workspace/{uuid.uuid4()}.mp3"
    with open(fileName, "wb") as file:
        file.write(response.content)
    
    audioFileLength = MP3(fileName).info.length
    audioFileLength = audioFileLength - (0.3) # remove pause between verses
    total_duration = total_duration + audioFileLength;
    
    # create the text clip
    
    quran_txt_clip = TextClip(
        font="./font.ttf",
        method='caption',
        text=text,
        size=(int(600 * multiplierWidth) , int(400 * multiplierHeight)),
        margin=(0,220 * multiplierHeight,0,25),
        text_align='center',
        vertical_align="bottom",
        font_size=int(50 * multiplierWidth),
        color='white',
        ).with_duration(audioFileLength)

    quran_txt_clip.audio = AudioFileClip(fileName)
    
    translation_txt_clip = TextClip(
        font="font/Tinos-Regular.ttf",
        method='caption',
        text=translation,
        size=(int(600 * multiplierWidth) , int(400 * multiplierHeight)),
        margin=(0,0,0,250 * multiplierHeight),
        text_align='center',
        vertical_align="top",
        font_size=int( 20 * multiplierWidth),
        color='white',
        
        ).with_duration(audioFileLength)
    
    translation_txt_clips.append(translation_txt_clip)

    txt_clips.append(quran_txt_clip)

clip = vfx.Loop(duration=total_duration + 1).apply(clip)

concat_txt_clips = concatenate_videoclips(txt_clips).with_position("top")
concat_translation_txt_clips = concatenate_videoclips(translation_txt_clips).with_position("bottom")

final_video = CompositeVideoClip([clip, concat_txt_clips, concat_translation_txt_clips])
final_video.write_videofile("result.mp4")


