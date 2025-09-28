import streamlit as st
import hashlib
import time
import random
import requests

# ====== Helper: Generate API Signature ======
def gen_sign(nonce, security_key, timestamp):
    keys = [str(nonce), str(security_key), str(timestamp)]
    keys.sort()
    key_str = ''.join(keys).encode('utf-8')
    signature = hashlib.sha1(key_str).hexdigest()
    return signature.lower()

# ====== Submit Task ======
def submit_task(api_key, security_key, image_url, audio_url):
    req_url = "https://cv-api.byteintlapi.com/api/common/v2/submit_task"
    timestamp = int(time.time())
    nonce = random.randint(0, (1 << 31) - 1)

    req_params = {
        "api_key": api_key,
        "timestamp": str(timestamp),
        "nonce": str(nonce),
        "sign": gen_sign(nonce, security_key, timestamp),
    }

    req_headers = {"Content-Type": "application/json"}

    req_body = {
        "req_key": "realman_avatar_picture_omni_cv",
        "image_url": image_url,
        "audio_url": audio_url,
    }

    resp = requests.post(req_url, params=req_params, headers=req_headers, json=req_body)
    return resp.json()

# ====== Query Task ======
def query_task(api_key, security_key, task_id):
    req_url = "https://cv-api.byteintlapi.com/api/common/v2/get_result"
    timestamp = int(time.time())
    nonce = random.randint(0, (1 << 31) - 1)

    req_params = {
        "api_key": api_key,
        "timestamp": str(timestamp),
        "nonce": str(nonce),
        "sign": gen_sign(nonce, security_key, timestamp),
    }

    req_headers = {"Content-Type": "application/json"}

    req_body = {
        "req_key": "realman_avatar_picture_omni_cv",
        "task_id": task_id,
    }

    resp = requests.post(req_url, params=req_params, headers=req_headers, json=req_body)
    return resp.json()

# ====== Streamlit UI ======
st.title("🎬 BytePlus API Demo")

st.sidebar.header("🔑 API Credentials")
api_key = st.sidebar.text_input("API Key", type="password")
security_key = st.sidebar.text_input("Security Key", type="password")

st.header("1️⃣ Submit Task")
image_url = st.text_input("Image URL", "https://xxxxx.jpg")
audio_url = st.text_input("Audio URL", "https://xxxxx.mp3")

if st.button("Submit Task"):
    if not api_key or not security_key:
        st.error("Please enter your API Key and Security Key in the sidebar.")
    else:
        response = submit_task(api_key, security_key, image_url, audio_url)
        st.json(response)
        if "data" in response and "task_id" in response["data"]:
            st.success(f"Task submitted! Task ID: {response['data']['task_id']}")
            st.session_state["task_id"] = response["data"]["task_id"]

st.header("2️⃣ Query Task Result")
task_id = st.text_input("Task ID", st.session_state.get("task_id", ""))

if st.button("Query Task"):
    if not api_key or not security_key:
        st.error("Please enter your API Key and Security Key in the sidebar.")
    elif not task_id:
        st.error("Please enter a Task ID.")
    else:
        response = query_task(api_key, security_key, task_id)
        st.json(response)
