import websocket
import datetime
import hashlib
import base64
import hmac
import json
import time
import ssl
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

def assess(APPID = 'ga6718ea', APIKey ='b7ae17b6e95b1b7cd1e9f0b1c13ecff5', APISecret = '0f0dfc033910e25a3d1d53dd18a3f9c7', AudioFile = 'turto/audio_data/audio.wav', Text = 'turto/text_data/user_speech.txt'):
    STATUS_FIRST_FRAME = 0  # Identification of the first frame
    STATUS_CONTINUE_FRAME = 1  # Identification of the middle frame
    STATUS_LAST_FRAME = 2  # Identification of the last frame

    # BusinessArgs parameter constants
    SUB = "ise"
    ENT = "en"
    CATEGORY = "read_sentence"
    
    # Initialize WebSocket parameters
    class Ws_Param(object):
        def __init__(self, APPID, APIKey, APISecret, AudioFile, Text):
            self.APPID = APPID
            self.APIKey = APIKey
            self.APISecret = APISecret
            self.AudioFile = AudioFile
            self.Text = Text
            self.CommonArgs = {"app_id": self.APPID}
            self.BusinessArgs = {"category": CATEGORY, "sub": SUB, "ent": ENT, "cmd": "ssb", "auf": "audio/L16;rate=16000",
                                 "aue": "raw", "text": self.Text, "ttp_skip": True, "aus": 1}

        def create_url(self):
            url = 'wss://ise-api-sg.xf-yun.com/v2/ise'
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))
            signature_origin = f"host: ise-api.xfyun.cn\ndate: {date}\nGET /v2/ise HTTP/1.1"
            signature_sha = hmac.new(self.APISecret.encode('utf-8'),
                                     signature_origin.encode('utf-8'),
                                     digestmod=hashlib.sha256).digest()
            signature = base64.b64encode(signature_sha).decode()
            authorization = base64.b64encode(
                f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'.encode('utf-8')
            ).decode()
            v = {"authorization": authorization, "date": date, "host": "ise-api.xfyun.cn"}
            return url + '?' + urlencode(v)

    wsParam = Ws_Param(APPID, APIKey, APISecret, AudioFile, Text)

    def on_message(ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print(f"sid:{sid} call error:{errMsg} code is:{code}")
            else:
                data = json.loads(message)["data"]
                if data["status"] == 2:
                    xml = base64.b64decode(data["data"])
                    # Write XML to file
                    with open("turto/text_data/assessment-point.xml", "w", encoding="utf-8") as f:
                        f.write(xml.decode("gbk"))
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_error(ws, error):
        print(f"### error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(ws):
        def run(*args):
            frameSize = 1280
            intervel = 0.04
            status = STATUS_FIRST_FRAME

            with open(wsParam.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    if not buf:
                        status = STATUS_LAST_FRAME
                    if status == STATUS_FIRST_FRAME:
                        d = {"common": wsParam.CommonArgs,
                             "business": wsParam.BusinessArgs,
                             "data": {"status": 0}}
                        ws.send(json.dumps(d))
                        status = STATUS_CONTINUE_FRAME
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"business": {"cmd": "auw", "aus": 2, "aue": "raw"},
                             "data": {"status": 1, "data": base64.b64encode(buf).decode()}}
                        ws.send(json.dumps(d))
                    elif status == STATUS_LAST_FRAME:
                        d = {"business": {"cmd": "auw", "aus": 4, "aue": "raw"},
                             "data": {"status": 2, "data": base64.b64encode(buf).decode()}}
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    time.sleep(intervel)
            ws.close()

        thread.start_new_thread(run, ())

    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == "__main__":
    assess(
        APPID='ga6718ea', APIKey='b7ae17b6e95b1b7cd1e9f0b1c13ecff5',
        APISecret='0f0dfc033910e25a3d1d53dd18a3f9c7', AudioFile='turto/audio_data/audio.wav', Text='turto/text_data/user_speech.txt'
    )
