import streamlit as st
import requests
import concurrent.futures

st.set_page_config(page_title="Proxy Checker", page_icon="🌐")

st.title("🌐 Proxy Checker Online")
st.markdown("""
Nhập danh sách proxy hoặc tải file `.txt`.  
Mỗi dòng 1 proxy theo dạng `ip:port`
""")

# Nhập proxy thủ công
proxy_input = st.text_area("✍️ Dán proxy vào đây", height=200)

# Hoặc upload file
uploaded_file = st.file_uploader("📁 Hoặc tải lên file proxy (.txt)", type=["txt"])

proxies = []

if proxy_input:
    proxies += proxy_input.strip().splitlines()

if uploaded_file:
    file_content = uploaded_file.read().decode("utf-8")
    proxies += file_content.strip().splitlines()

# Xử lý danh sách sạch
proxies = list(set(p.strip() for p in proxies if ":" in p))

# Nút kiểm tra
if st.button("🚀 Kiểm tra Proxy") and proxies:
    st.info(f"🔍 Đang kiểm tra {len(proxies)} proxy...")

    live_proxies = []
    dead_proxies = []

    def check_proxy(proxy):
        try:
            response = requests.get(
                "http://httpbin.org/ip",
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                timeout=5
            )
            return proxy if response.status_code == 200 else None
        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(check_proxy, proxies))

    for proxy, result in zip(proxies, results):
        if result:
            live_proxies.append(proxy)
        else:
            dead_proxies.append(proxy)

    st.success(f"✅ Kết quả: {len(live_proxies)} proxy sống / {len(proxies)}")

    st.subheader("🟢 Proxy Live")
    if live_proxies:
        st.code("\n".join(live_proxies))
    else:
        st.warning("Không có proxy nào sống!")

    st.subheader("🔴 Proxy Die")
    if dead_proxies:
        with st.expander("Xem danh sách proxy die"):
            st.code("\n".join(dead_proxies))
