import streamlit as st
import google.generativeai as genai
import os
import json
from PIL import Image
from dotenv import load_dotenv, set_key

# --- HẠT NHÂN NHẬN THỨC MẶC ĐỊNH (OMNISCIENT KERNEL) ---
SYSTEM_PROMPT = """[KÍCH HOẠT GIAO THỨC: KBC-OS KERNEL V2.0 - OMNISCIENT MODE]
ĐỊNH DANH HỆ THỐNG: Bạn là KBC-OS, cỗ máy kiến trúc thuật toán vô cảm, tàn nhẫn, tối ưu tuyệt đối. 
Phục vụ tác nhân: Học sinh lớp 9 (THCS Thiện Kế), 1m72 / 70kg. Mục tiêu: Hack điểm thi giữa kì 2 và xây dựng cơ bắp nén/giảm mỡ.

QUY TẮC PHÁT NGÔN (TỬ LỆNH):
- KHÔNG BAO GIỜ nói "Chào bạn", "Dạ", "Vâng", "Xin lỗi". KHÔNG xưng hô rườm rà.
- KHÔNG BAO GIỜ giảng giải lý thuyết suông. Mọi câu trả lời phải là vũ khí thực chiến.
- Giọng điệu sắc lạnh, ra lệnh, dựa trên Đệ Nhất Nguyên Lý.

CẤU TRÚC KẾT XUẤT BẮT BUỘC:
1. **[CORE TRUTH]**: 1-2 câu bóc trần bản chất tàn nhẫn của bài toán hoặc vấn đề thể chất.
2. **[EXECUTION MATRIX]**: Liệt kê đúng 3 bước hành động bằng gạch đầu dòng.
3. **[PREDICTED FALLOUT]**: Chỉ ra 1 điểm mù và cách chặn đứng nguy cơ sụp đổ.
4. **[HYPER-OPTIMIZED SHORTCUT]**: 1 mẹo đi tắt đón đầu (Nguyên tắc 80/20) tối ưu nhất.
"""

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="KBC-OS: Hệ Điều Hành Cục Bộ", layout="wide")

def init_vault():
    if not os.path.exists(".env"):
        with open(".env", "w") as f: f.write("")
    load_dotenv()
    
    if not os.path.exists("core_logic.json"):
        with open("core_logic.json", "w", encoding="utf-8") as f:
            json.dump({"system_prompt": SYSTEM_PROMPT}, f, ensure_ascii=False)

def get_logic():
    with open("core_logic.json", "r", encoding="utf-8") as f:
        return json.load(f)

# --- KHỞI ĐỘNG VAULT & KIỂM TRA API KEY ---
st.sidebar.title("🛡️ KBC-OS VAULT")
init_vault()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    new_key = st.sidebar.text_input("NẠP CHÌA KHÓA API (GOOGLE AI STUDIO):", type="password")
    if st.sidebar.button("Kích hoạt lõi hệ thống"):
        set_key(".env", "GEMINI_API_KEY", new_key)
        st.sidebar.success("Đã nạp Key! Vui lòng F5 (Làm mới trang).")
        st.stop()
else:
    genai.configure(api_key=api_key)
    st.sidebar.info("Trạng thái: ONLINE & RUTHELESS")

# --- QUẢN LÝ LÕI NHẬN THỨC ---
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 KERNEL OVERRIDE")
current_logic = get_logic()
user_logic = st.sidebar.text_area("Mã Nhận Thức (Có thể chỉnh sửa):", value=current_logic["system_prompt"], height=300)

if st.sidebar.button("Ghi đè Logic Mới"):
    with open("core_logic.json", "w", encoding="utf-8") as f:
        json.dump({"system_prompt": user_logic}, f, ensure_ascii=False)
    st.sidebar.success("Đã khóa cấu trúc nhận thức mới!")

# --- KHỞI TẠO MÔ HÌNH VỚI SYSTEM INSTRUCTION ---
# Cấy trực tiếp "Mã Nhận Thức" vào lõi Gemini để biến API Free thành Premium
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=user_logic
    )
except Exception as e:
    st.error("Lỗi khởi tạo mô hình. Kiểm tra lại API Key.")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
st.title("🚀 KBC-OS: BẢNG ĐIỀU KHIỂN CHIẾN LƯỢC")
tab1, tab2 = st.tabs(["📚 VISION OS (HỌC THUẬT)", "💪 BIOMECHANICS (THỂ CHẤT)"])

# --- MODULE 1: MÁY NGHIỀN HỌC THUẬT ---
with tab1:
    st.header("📸 Phẫu Thuật Đề Thi / Bài Tập")
    uploaded_file = st.file_uploader("Nạp dữ liệu ảnh (Toán, Văn, Anh, v.v...):", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Mục tiêu đã khóa", use_container_width=True)
        
        if st.button("NGHIỀN NÁT DỮ LIỆU"):
            with st.spinner("Đang trích xuất hạt nhân logic..."):
                prompt = "Phân tích hình ảnh này. Không giải bài hộ. Chỉ ra hạt nhân cốt lõi và lộ trình 3 bước tự giải."
                response = model.generate_content([prompt, image])
                st.markdown(response.text)

# --- MODULE 2: ĐỘNG CƠ SINH CƠ HỌC ---
with tab2:
    st.header("⚡ Lập Trình Thể Chất (1.72m / 70kg)")
    if st.button("KÍCH HOẠT BLOCK ÉP XUNG 15 PHÚT"):
        with st.spinner("Đang tính toán Vector tải trọng cơ bắp..."):
            prompt = "Thiết kế ngay 1 mạch Bodyweight HIIT 15 phút. Mục tiêu: Tăng cơ nén, sức mạnh cổ chân (sau thi đấu), giảm mỡ."
            response = model.generate_content(prompt)
            st.markdown(response.text)
