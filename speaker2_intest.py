import requests
import os

def speech_to_text_from_file(api_key: str, file_path: str) -> str:
    """
    Chuyển âm thanh từ file WAV thành văn bản bằng FPT.AI Speech-to-Text API.

    Args:
        api_key (str): FPT.AI API key.
        file_path (str): Đường dẫn đến file âm thanh WAV.

    Returns:
        str: Kết quả nhận dạng hoặc thông báo lỗi.
    """
    print(f"Đang xử lý file âm thanh: {file_path}...")

    try:
        # Kiểm tra file có tồn tại không
        if not os.path.exists(file_path):
            return f"[Lỗi] File {file_path} không tồn tại!"

        print("Gửi file âm thanh lên FPT.AI...")

        # Gửi file đến FPT API
        with open(file_path, 'rb') as f:
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

if __name__ == "__main__":
    file_path = "test.wav"
    result = speech_to_text_from_file("MQiJQGGgD9JVHFkPDIyYuwSG3gATaBCr", file_path)
    print("Kết quả cuối cùng:", result)
