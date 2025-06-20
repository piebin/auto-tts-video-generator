from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import *
from moviepy.config import change_settings
from datetime import datetime
import os

# === 경로 설정 ===
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
change_settings({
    "IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-6.9.13-Q16-HDRI/convert.exe"
})

# === 설정값 ===
VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280
if VIDEO_WIDTH % 2 != 0: VIDEO_WIDTH += 1
if VIDEO_HEIGHT % 2 != 0: VIDEO_HEIGHT += 1

CAPTION_WIDTH = 680
FONT_SIZE = 72
FONT_PATH = "C:/Windows/Fonts/HMKMRHD.TTF"  # 한글 지원 폰트

# === 대본 입력 ===
print("\n🎤 대본을 입력하세요. 여러 줄 입력 후 Ctrl+Z (Windows) / Ctrl+D (Mac/Linux) 로 종료:")
lines = []
try:
    while True:
        line = input()
        if line.strip(): lines.append(line.strip())
except EOFError:
    pass

# === 영상 입력 ===
video_input = input("\n🎬 사용할 배경 영상 경로들을 mp4 단위로 입력하세요:\n> ").strip()
video_paths = [v.strip() for v in video_input.split(".mp4") if v.strip()]
video_paths = [vp + ".mp4" for vp in video_paths]

# === TTS 속도 입력 ===
print("\n🚀 TTS 속도를 선택하세요 (기본값: 1.0):\n예시: 1.0 (보통), 1.5 (빠름), 0.8 (느림)")
try:
    tts_speed = float(input("> ").strip() or "1.0")
except ValueError:
    print("⚠️ 잘못된 입력입니다. 기본 속도 1.0 사용.")
    tts_speed = 1.0

# === 자막 위치 선택 ===
print("\n📍 자막 위치를 선택하세요:\n1 - 상단\n2 - 중앙\n3 - 하단 (기본)")
position_input = input("> ").strip()
position_map = {"1": "top", "2": "center", "3": "bottom"}
subtitle_position = position_map.get(position_input, "bottom")

# === 출력 폴더 ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"local_video_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

# === 영상 병합 ===
video_clips = []
for path in video_paths:
    clip = VideoFileClip(path).resize((VIDEO_WIDTH, VIDEO_HEIGHT))
    video_clips.append(clip)
combined_video = concatenate_videoclips(video_clips, method="compose")

# === TTS mp3 생성 및 속도 조정 ===
final_audio_segments = []
line_durations = []

for idx, line in enumerate(lines):
    tts = gTTS(text=line, lang='ko')
    temp_mp3 = os.path.join(output_dir, f"line_{idx}.mp3")
    tts.save(temp_mp3)

    audio = AudioSegment.from_file(temp_mp3)
    if tts_speed != 1.0:
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * tts_speed)
        }).set_frame_rate(audio.frame_rate)

    final_audio_segments.append(audio)
    duration_sec = len(audio) / 1000.0
    line_durations.append(duration_sec)

# === 전체 오디오 합치기 ===
full_audio = sum(final_audio_segments)
full_audio_path = os.path.join(output_dir, "voice_final.mp3")
full_audio.export(full_audio_path, format="mp3")
audio_clip = AudioFileClip(full_audio_path)
audio_duration = audio_clip.duration

# === 배경 영상 길이 맞추기 ===
if combined_video.duration < audio_duration:
    loop_count = int(audio_duration // combined_video.duration) + 1
    combined_video = concatenate_videoclips([combined_video] * loop_count, method="compose")
combined_video = combined_video.subclip(0, audio_duration)

# === 자막 생성 ===
subtitles = []
start_time = 0
for i, line in enumerate(lines):
    duration = line_durations[i]
    txt_clip = TextClip(line,
                        fontsize=FONT_SIZE,
                        font=FONT_PATH,
                        color='white',
                        size=(CAPTION_WIDTH, None),
                        method='caption')
    height = txt_clip.h + 40
    if height % 2 != 0: height += 1

    txt_clip = txt_clip.on_color(size=(CAPTION_WIDTH, height),
                                 color=(0, 0, 0),
                                 col_opacity=0.6)
    txt_clip = txt_clip.set_position(subtitle_position).set_duration(duration).set_start(start_time)
    subtitles.append(txt_clip)
    start_time += duration

# === 영상 합성 ===
final = CompositeVideoClip([combined_video.set_audio(audio_clip)] + subtitles).set_duration(audio_duration)

# === 렌더링 ===
output_path = os.path.join(output_dir, "final_video.mp4")
final.write_videofile(output_path,
                      fps=24,
                      codec="libx264",
                      audio_codec="aac",
                      ffmpeg_params=["-pix_fmt", "yuv420p"])

print(f"\n🎞️ 영상 생성 완료!\n📍 위치: {output_path}")
