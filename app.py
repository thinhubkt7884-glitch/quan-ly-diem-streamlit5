import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")

# 1. Khởi tạo dữ liệu
@st.cache_data
def load_data():
    data = {
        'Họ và tên': [
            'Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D', 'Hoàng Văn E',
            'Vũ Thị F', 'Đặng Văn G', 'Bùi Thị H', 'Đỗ Văn I', 'Nông Thị K'
        ],
        'Chuyên cần': [8.5, 9.0, 7.0, 6.5, 9.5, 5.0, 8.0, 7.5, 6.0, 10.0],
        'Giữa kỳ':    [7.0, 8.5, 6.0, 5.5, 9.0, 4.5, 7.5, 8.0, 5.0, 9.5],
        'Cuối kỳ':    [8.0, 9.0, 5.5, 4.0, 9.5, 4.0, 8.5, 7.0, 5.5, 9.0]
    }
    df = pd.DataFrame(data)
    
    # Tính điểm tổng kết
    df['Tong_ket'] = (0.20 * df['Chuyên cần'] + 0.30 * df['Giữa kỳ'] + 0.50 * df['Cuối kỳ']).round(2)
    
    # Xếp loại
    def xep_loai(diem):
        if diem >= 8.5: return 'Giỏi'
        elif diem >= 7.0: return 'Khá'
        elif diem >= 5.0: return 'Trung bình'
        else: return 'Yếu'
        
    df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)
    return df

df = load_data()

# 2. Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# 3. Bảng điểm đầy đủ
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 4. Thống kê tổng quan
st.subheader("📊 Thống kê chung")
col1, col2, col3, col4 = st.columns(4)

dtb_lop = df['Tong_ket'].mean()
sv_caonhat = df.loc[df['Tong_ket'].idxmax()]
sv_thapnhat = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()

col1.metric("ĐTB Của Lớp", f"{dtb_lop:.2f}")
col2.metric("Điểm Cao Nhất", f"{sv_caonhat['Tong_ket']}", f"{sv_caonhat['Họ và tên']}")
col3.metric("Điểm Thấp Nhất", f"{sv_thapnhat['Tong_ket']}", f"{sv_thapnhat['Họ và tên']}")
col4.metric("Số SV Đạt (≥5.0)", f"{so_sv_dat}/{len(df)}")

st.markdown("---")

# 5. Danh sách chọn sinh viên (Selectbox)
st.subheader("🔍 Tra cứu sinh viên")
selected_student = st.selectbox("Chọn sinh viên để xem chi tiết:", df['Họ và tên'].unique())

if selected_student:
    sv_info = df[df['Họ và tên'] == selected_student].iloc[0]
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.write(f"**Chuyên cần:** {sv_info['Chuyên cần']}")
    c2.write(f"**Giữa kỳ:** {sv_info['Giữa kỳ']}")
    c3.write(f"**Cuối kỳ:** {sv_info['Cuối kỳ']}")
    c4.write(f"**Tổng kết:** {sv_info['Tong_ket']}")
    c5.write(f"**Xếp loại:** {sv_info['Xep_loai']}")

st.markdown("---")

# 6. Biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(df['Họ và tên'], df['Tong_ket'], color='#4C72B0', edgecolor='black')

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval}', ha='center', va='bottom', fontsize=8)

ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10.5)
plt.xticks(rotation=30)
plt.grid(axis='y', linestyle='--', alpha=0.5)

st.pyplot(fig)

# 7. Thông tin sinh viên thực hiện (chữ nhỏ ở chân trang)
st.markdown("---")
st.markdown("<p style='font-size: 12px; color: gray; text-align: center;'>Họ và tên người thực hiện: Ưng Hoàng Gia Thịnh | MSSV: 064208011821</p>", unsafe_allow_html=True)