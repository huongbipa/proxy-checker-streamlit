import streamlit as st
import requests
import concurrent.futures

# Kiểm tra API Key từ zeroios.net
def check_api_key(api_key):
    try:
        url = f"https://zeroios.net/check_key.php?key={api_key}"
        response = requests.get(url, timeout=5)
        if "success" in response.text.lower() or "valid" in response.text.lower():
            return True
    except:
        pass
    return False

# Cấu hình giao diện
st.set_page_config(page_title="Proxy Checker", page_icon="🧪")
st.title("🧪 Proxy Checker Online có Xác Thực API Key")

# Bước 1: Nhập API Key
api_key = st.text_input("🔑 Nhập API Key:", type="password")

# Kiểm tra key
if api_key:
    if check_api_key(api_key):
        st.success("✅ API Key hợp lệ. Bạn có thể sử dụng tool.")

        # Bước 2: Nhập proxy thủ công hoặc upload file
        st.subheader("📥 Nhập Proxy cần kiểm tra")
        proxy_input = st.text_area("✍️ Dán proxy (ip:port) mỗi dòng", height=200)
        uploaded_file = st.file_uploader("📁 Hoặc tải file .txt", type=["txt"])

        proxies = []
        if proxy_input:
            proxies += proxy_input.strip().splitlines()
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            proxies += content.strip().splitlines()

        # Lọc proxy hợp lệ
        proxies = list(set(p.strip() for p in proxies if ":" in p))

        if st.button("🚀 Kiểm tra Proxy") and proxies:
            st.info(f"🔍 Đang kiểm tra {len(proxies)} proxy...")

            live_proxies = []
            dead_proxies = []

            def check_proxy(proxy):
                try:
                    res = requests.get(
                        "http://httpbin.org/ip",
                        proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                        timeout=5
                    )
                    return proxy if res.status_code == 200 else None
                except:
                    return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                results = list(executor.map(check_proxy, proxies))

            for proxy, result in zip(proxies, results):
                if result:
                    live_proxies.append(proxy)
                else:
                    dead_proxies.append(proxy)

            st.success(f"✅ Đã kiểm tra xong. {len(live_proxies)} proxy sống / {len(proxies)} tổng.")

            st.subheader("🟢 Proxy Sống")
            if live_proxies:
                st.code("\n".join(live_proxies))
            else:
                st.warning("Không có proxy nào sống.")

            st.subheader("🔴 Proxy Die")
            if dead_proxies:
                with st.expander("Xem danh sách Proxy Die"):
                    st.code("\n".join(dead_proxies))
    else:
        st.error("❌ API Key không hợp lệ hoặc hết hạn.")
else:
    st.info("🔐 Vui lòng nhập API Key để bắt đầu sử dụng.")
