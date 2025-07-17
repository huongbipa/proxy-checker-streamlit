import streamlit as st
import requests

st.set_page_config(page_title="Get Proxy V9", page_icon="🕵️")

st.title("🕵️ Get Proxy V9 - Tool Thu Thập Proxy Mới Nhất")
st.markdown("""
✅ Phiên bản: **9.0**  
🗓️ Cập nhật ngày: **22/03/2025**  
👤 Tác giả: **Cá Tool - Dương Ngọc 💘 Quỳnh Anh**  
""")

proxy_links = [
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
    "https://proxyspace.pro/https.txt",
    "https://proxyspace.pro/http.txt"
]

start = st.button("🚀 Bắt đầu thu thập proxy")

if start:
    proxies = []
    status = st.empty()

    for site in proxy_links:
        try:
            status.info(f"🔄 Đang tải từ: {site}")
            response = requests.get(site, timeout=10, verify=False)
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if ':' in line and len(line.split(':')) == 2:
                        ip, port = line.strip().split(":")
                        proxies.append(f"{ip}:{port}")
        except Exception as e:
            st.warning(f"⚠️ Lỗi tải {site}")

    proxies = list(set(proxies))  # loại trùng

    st.success(f"✅ Thu thập hoàn tất! Tổng số proxy: {len(proxies)}")

    # Hiển thị danh sách proxy
    st.code("\n".join(proxies), language='text')
