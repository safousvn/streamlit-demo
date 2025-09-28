import hashlib 
import time 
import random 
import requests 
 
 
def gen_sign(nonce, security_key, timestamp): 
    keys = [str(nonce), str(security_key), str(timestamp)] 
    keys.sort() 
    key_str = ''.join(keys).encode('utf-8') 
    signature = hashlib.sha1(key_str).hexdigest() 
    return signature.lower() 
 
 
if __name__ == '__main__':
    req_url = 'https://cv-api.byteintlapi.com/api/common/v2/submit_task' 
    timestamp = int(time.time()) 
    nonce = random.randint(0, (1 << 31) - 1) 
    req_params = {  # Query parameters
        "api_key": "your_ak",
        "timestamp": str(timestamp),
        "nonce": str(nonce),
        "sign": gen_sign(nonce, "your_sk", timestamp)
    } 
    req_headers = {
        "Content-Type": "application/json" 
    } 
    req_body = {  # Body parameters
        "req_key": "realman_avatar_picture_omni_cv",
        "image_url": "https://xxxxx.jpg",
        "audio_url": "https://xxxxx.mp3"
    } 
 
    resp = requests.post(req_url, params=req_params, headers=req_headers, json=req_body) 
    print(resp.json()) 
