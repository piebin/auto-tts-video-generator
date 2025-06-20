# auto-tts-video-generator
A simple Korean TTS video generator with subtitle syncing and background merging.

**자동으로 대본을 음성(TTS)과 자막이 포함된 영상으로 만들어주는 Python 스크립트**

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![MoviePy](https://img.shields.io/badge/Library-MoviePy-orange)
![gTTS](https://img.shields.io/badge/TTS-gTTS-lightgrey)
![Status](https://img.shields.io/badge/Status-Ready-brightgreen)

---

## 📌 주요 기능

- 🎤 입력한 대본을 **한국어 TTS 음성**으로 변환
- 🎞️ 배경 영상(mp4)을 여러 개 병합하여 자동 재생
- 📝 입력한 대본을 **엔터 기준으로 자막 분할**하여 자동 표시
- ⏱️ 자막 타이밍은 TTS 속도에 맞춰 자동 계산
- 🔠 자막 위치 선택: 상단 / 중단 / 하단
- ⚙️ TTS 속도(1.0, 1.5, 2.0 등) 자유롭게 설정 가능

---

## 🔧 설치 방법

### 1. 필수 프로그램 설치
- [Python 3.9 이상](https://www.python.org/downloads/)
- [FFmpeg (Windows용 zip)](https://www.gyan.dev/ffmpeg/builds/)
    - 다운로드 후 `ffmpeg.exe` 경로를 `C:\ffmpeg\bin\ffmpeg.exe`로 설정
- [ImageMagick 6.9.13-Q16-HDRI](https://imagemagick.org/download/binaries/ImageMagick-6.9.13-7-Q16-x64-dll.exe)
    - 코드에 절대주소로 명시했기에, C:/Program Files/ImageMagick-6.9.13-Q16-HDRI 에 설치 필요

### 2. 프로젝트 클론 및 패키지 설치

```bash
git clone https://github.com/piebin/auto-tts-video-generator.git
cd auto-tts-video-generator
pip install -r requirements.txt



🔤 한글 폰트 주의사항

자막에 사용할 한글 폰트는 시스템 폰트 중 하나인 HY헤드라인M (HMKMRHD.TTF) 를 사용합니다.
저작권 문제 없는 무료 배포 폰트입니다.

📄 라이선스
MIT License




