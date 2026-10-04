import streamlit as st

# Cài đặt tiêu đề trang
st.set_page_config(page_title="Tính Lãi Tiết Kiệm", page_icon="💰")
st.title("Ứng dụng tính lãi gửi tiết kiệm 💰")

# Form nhập liệu
st.header("1. Nhập thông tin gửi tiền")
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input("Số tiền gửi (VNĐ)", min_value=0.0, step=1000000.0, format="%.0f")
    ky_han = st.number_input("Kỳ hạn (tháng)", min_value=1, step=1)
    lai_suat = st.number_input("Lãi suất (%/năm)", min_value=0.0, step=0.1, format="%.2f")

with col2:
    loai_lai = st.selectbox("Hình thức tính lãi", ["Lãi đơn", "Lãi kép"])
    hinh_thuc_lanh_lai = st.selectbox("Hình thức lãnh lãi", ["Lãnh lãi cuối kỳ", "Lãnh lãi hàng tháng", "Lãnh lãi hàng quý"])

# Nút bấm tính toán
if st.button("Tính toán", type="primary"):
    # Đổi dữ liệu để tính toán
    r = lai_suat / 100
    t = ky_han / 12  # Đổi tháng ra năm
    
    tong_tien_lai = 0
    tong_goc_lai = 0
    lai_dinh_ky = 0
    
    # Tính số kỳ lãnh lãi
    so_ky_lanh_lai = 1
    if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
        so_ky_lanh_lai = ky_han
    elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
        so_ky_lanh_lai = ky_han / 3

    # Công thức tính
    if loai_lai == "Lãi đơn":
        tong_tien_lai = so_tien_gui * r * t
        tong_goc_lai = so_tien_gui + tong_tien_lai
        
    else: # Lãi kép
        n = 1 # Số lần ghép lãi trong năm
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            n = 12
        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            n = 4
        
        # Tính tổng tiền gốc và lãi cuối kỳ
        tong_goc_lai = so_tien_gui * ((1 + r/n) ** (n * t))
        tong_tien_lai = tong_goc_lai - so_tien_gui

    # Tính tiền lãi định kỳ (nếu không phải cuối kỳ)
    if hinh_thuc_lanh_lai != "Lãnh lãi cuối kỳ" and so_ky_lanh_lai > 0:
        lai_dinh_ky = tong_tien_lai / so_ky_lanh_lai

    # Hiển thị kết quả
    st.header("2. Kết quả tính toán")
    
    st.success(f"**Tổng số tiền gốc và lãi:** {tong_goc_lai:,.0f} VNĐ")
    st.info(f"**Tổng tiền lãi nhận được:** {tong_tien_lai:,.0f} VNĐ")
    
    if hinh_thuc_lanh_lai != "Lãnh lãi cuối kỳ":
        st.warning(f"**Tiền lãi nhận định kỳ (trung bình):** {lai_dinh_ky:,.0f} VNĐ / kỳ")
