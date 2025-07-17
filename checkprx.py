import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="Check Proxy Tool", page_icon="🛠️")

st.title("🛠️ Proxy Checker Web Tool")
st.markdown("Chuyển từ bản terminal sang bản web để check proxy nhanh chóng.")

uploaded_file = st.file_uploader("📁 Upload file proxy (dạng ip:port mỗi dòng)", type=["txt"])
num_threads = st.slider("Số luồng kiểm tra đồng thời", min_value=1, max_value=500, value=100)
start_button = st.button("🚀 Bắt đầu kiểm tra")

proxy_live = []
status_display = st.empty()

def check_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=3)
        if response.status_code in [200, 202, 500, 502, 503, 504]:
            return proxy
    except:
        pass
    return None

def detect_location(proxy):
    ip = proxy.split(':')[0]
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = r.json()
        if data.get("status") == "success":
            return f"{data['country']} / {data['city']}"
    except:
        pass
    return "Không rõ"

if uploaded_file and start_button:
    content = uploaded_file.read().decode('utf-8')
    proxy_list = [line.strip() for line in content.splitlines() if line.strip()]

    status_display.info(f"Đang kiểm tra {len(proxy_list)} proxy...")
    results = []

    def process(proxy):
        result = check_proxy(proxy)
        if result:
            location = detect_location(result)
            proxy_live.append((result, location))
            status_display.success(f"✅ {result} - {location}")
        else:
            status_display.warning(f"❌ {proxy} - Die")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process, proxy_list)

    st.success(f"✅ Hoàn tất! Tổng số proxy live: {len(proxy_live)}")

    if proxy_live:
        live_text = "\n".join([f"{prx[0]} # {prx[1]}" for prx in proxy_live])
        st.download_button("⬇️ Tải danh sách proxy live", data=live_text, file_name="proxy_live.txt")
