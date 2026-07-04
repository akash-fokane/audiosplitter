from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from pydub.playback import play
import librosa
from spleeter.separator import Separator
# import yt_dlp

# def stream_youtube_audio(url):
#     ydl_opts = {
#         'format': 'ba* / b',
#         # outtmpl '-' tells yt-dlp to stream to stdout
#         'outtmpl': '-',
#         'logtostderr': True,  # Keeps logs out of the stdout stream
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         # Extract info to get the direct stream URL
#         info = ydl.extract_info(url, download=False)
#         stream_url = info['url']
#         sample_rate = info.get('asr', 44100)
        
#         # You can now pass this direct 'stream_url' to modules like cv2, librosa, etc.
#         print(f"Direct Stream URL: {stream_url}")
#         return stream_url, sample_rate

def readmp3(f):
    print(f"Reading file {f}")
    audio = AudioSegment.from_mp3(f)
    channels = audio.channels
    frame_rate = audio.frame_rate
    y = np.array(audio.get_array_of_samples(),dtype=np.float32)

    if audio.channels == 2:
        y = y.reshape((-1,2)).T

    return channels, frame_rate, y/32768.0

def exportmp3(reconstruct_channels, sample_rate, filename):
    stereo_signal = np.vstack(reconstruct_channels)
    stereo_signal = (stereo_signal*32767.0).astype(np.int16)
    stereo_signal = stereo_signal.T.flatten()

    output = AudioSegment(
        data=stereo_signal.tobytes(),
        sample_width=2,
        frame_rate = sample_rate,
        channels=2,
    )

    print(f"exporting to {filename}")
    output.export(filename,format="mp3")

def process(raw_array):
    raw_channels = raw_array.T
    reconstruct_list = []

    for i in range(raw_channels.shape[0]):
        stft_matrix = librosa.stft(raw_channels[i])
        reconstruct_t = librosa.istft(stft_matrix)
        reconstruct_list.append(reconstruct_t)

    return reconstruct_list


def split_song(input_file, vocals_file, instruments_file):

    # video_url = "https://www.youtube.com/watch?v=GX9x62kFsVU"
    # audio_stream, sample_rate = stream_youtube_audio(video_url)

    channels, sample_rate, mysong = readmp3(input_file)

    # mysong, sample_rate = librosa.load(audio_stream, sr=sample_rate, mono=False)

    spleeter_input = mysong.T

    separator = Separator("spleeter:2stems")
    prediction = separator.separate(spleeter_input)

    processed_vocal = process(prediction["vocals"])
    exportmp3(processed_vocal, sample_rate, vocals_file)

    processed_vocal = process(prediction["accompaniment"])
    exportmp3(processed_vocal, sample_rate, instruments_file)


def main():
    split_song("dhurandhar.mp3", "vocals.mp3", "instruments.mp3")

if __name__ == "__main__":
    main()
