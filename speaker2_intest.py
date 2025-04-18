import sounddevice as sd
from scipy.io.wavfile import write
import requests
import tempfile
import os

def speech_to_text_from_mic(api_key: str, duration: int = 5, fs: int = 16000) -> str:
    """
    Ghi âm từ microphone và chuyển thành văn bản bằng FPT.AI Speech-to-Text API.

    Args:
        api_key (str): FPT.AI API key.
        duration (int): Thời lượng ghi âm (giây).
        fs (int): Tần số lấy mẫu. FPT yêu cầu 16000 Hz.

    Returns:
        str: Kết quả nhận dạng hoặc thông báo lỗi.
    """
    print(f"Ghi âm trong {duration} giây...")

    try:
        # Ghi âm từ mic
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        # Lưu file tạm
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            write(tmpfile.name, fs, recording)
            audio_path = tmpfile.name

        print("Gửi file âm thanh lên FPT.AI...")

        # Gửi file đến FPT API
        with open(audio_path, 'rb') as f:
            headers = {
                "api-key": api_key,
                "Content-Type": "audio/wav"
            }
            response = requests.post("https://api.fpt.ai/hmi/asr/general", headers=headers, data=f)

        print(f"Mã phản hồi HTTP: {response.status_code}")
        print("Nội dung phản hồi từ FPT:", response.text)

        # Phân tích kết quả
        if response.status_code == 200:
            result = response.json()
            if "hypotheses" in result and result["hypotheses"]:
                text = result["hypotheses"][0]["utterance"]
                print("Kết quả nhận dạng:", text)
                return text
            else:
                return "[Không có kết quả nhận dạng hoặc âm thanh không rõ]"
        else:
            return f"[Lỗi HTTP {response.status_code}] {response.text}"

    except Exception as e:
        return f"[Lỗi hệ thống] {str(e)}"

    finally:
        # Dọn file tạm
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    result = speech_to_text_from_mic("MQiJQGGgD9JVHFkPDIyYuwSG3gATaBCr")
    print("Kết quả cuối cùng:", result)
