import streamlit as st
import pandas as pd
import io
# Đọc dữ liệu từ file Excel
df = pd.read_excel("./Book1.xlsx")
sf = pd.read_excel("./result.xlsx")
excel_file = "result.xlsx"
# Khai báo giá trị k để so sánh
def write_to_excel(ks, row, d, excel_file):
    row1 = row + 1
    ab = st.session_state.get("ex", None)
    gf = pd.DataFrame([ab])
    with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists='overlay') as writer:
        gf.to_excel(writer, startrow=row1, startcol=d, index=False, header=False)
    return
# Danh sách để lưu số hàng thỏa mãn điều kiện
#bd = st.number_input("Biên độ của cầu")
nd = int(st.number_input("Số ngày soi cầu"))
#nd = 3
jd = int(st.number_input("Số ngày bạn muốn tính kết quả:"))
bd = 1
#if bd == 0 :
    #bd = 5
    #st.write("Bên độ soi cầu là: ",bd)
num_r = []
numx = []
numy = []
num_d = []
# Duyệt qua các hàng của DataFrame
#st.write("Ngày dừng lại để tính toán",df.iloc[kd, 0])
if st.button("Nhấn nút này để tính toán"):
    my_bar = st.progress(0)
    for kd in range(1,jd):
        my_bar.progress(((kd)/(jd-1)), "Đang tính toán, vui lòng đợi:")
        if nd > 2:
            for u in range(0, nd):
                x_u = str(int(df.iloc[u+kd, 1]))[-2:]
                y_u = df.iloc[u, 0]
                numx.append(x_u)
                numy.append(y_u)
                #if u > 0:
                    #st.write(int(numx[u]) - int(numx[u-1]))
        #st.write(str(numx),df.iloc[0, 0])
        #st.write(kd)
        for bd in range(1,16):
            #st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
            #st.write(kd)
            if nd > 2:
                kml = kd + 1
                for i in range(kml,len(df)-20):
                    l = int(str(int(df.iloc[i, 1]))[-2:])  # Lấy hai ký tự cuối cùng của giá trị và chuyển thành chuỗi
                    l1 = int(str(int(df.iloc[i + 1, 1]))[-2:])
                    x1 = l1 - l
                    if (int(numx[1]) - int(numx[0])) - bd <= x1 <= (int(numx[1]) - int(numx[0])) + bd:
                        match_found = True
                        for p in range(2, nd):
                            l_p = int(str(int(df.iloc[i+p, 1]))[-2:])
                            l_f = int(str(int(df.iloc[i+p-1, 1]))[-2:])
                            x_p = l_p - l_f
                            if (int(numx[p]) - int(numx[p-1]))- bd <= x_p <= (int(numx[p]) - int(numx[p-1])) + bd:
                                if p == nd - 1:
                                    lits=[]
                                    for m in range(0,nd):
                                        pl = i+m
                                        lits.append(df.iloc[pl, 1])
                                    num_r.append(str(int(df.iloc[i-1, 1]))[-2:])
                                    #st.write(df.iloc[i, 0])
                                    #st.write(lits,)
                                    #st.write(str(int(df.iloc[i-1, 1]))[-2:])
                            else:
                                break
                #st.write("Các chỉ số hàng thỏa mãn điều kiện:")
                #st.write(str(num_r))
                tl = len(num_r)
                #st.write(tl)
                #st.write(nd)
                lon = 0
                be = 0
                for nu in range(0,tl):
                    kh = int(num_r[nu])
                    if kh > 50:
                        lon = lon + 1
                    else:
                        be = be + 1
                ks = df.iloc[kd, 0]
                st.session_state["ex"] = ks
                write_to_excel(ks, kd, 0, excel_file)
                if tl != 0:
                    #st.write("Số cầu thõa mãn là :",tl)
                    if round((lon/tl)*100,2) > round((be/tl)*100,2):
                        if round((lon/tl)*100,2) > 50 and df.iloc[i-1, 1] > 50:
                            ks = "Thắng"
                            st.session_state["ex"] = ks
                            write_to_excel(ks, kd, bd, excel_file)
                        else:
                            ks = "Thua"
                            st.session_state["ex"] = ks
                            write_to_excel(ks, kd, bd, excel_file)
                    else:
                        if round((be / tl) * 100, 2) > 50 and df.iloc[i - 1, 1] < 50:
                            ks = "Thắng"
                            st.session_state["ex"] = ks
                            write_to_excel(ks, kd, bd, excel_file)
                        else:
                            ks = "Thua"
                            st.session_state["ex"] = ks
                            write_to_excel(ks, kd, bd, excel_file)
                else:
                    ks = "Không có"
                    st.session_state["ex"] = ks
                    write_to_excel(ks, kd, bd, excel_file)
                num_r = []
        numx = []
        numy = []
    data = pd.read_excel("./result.xlsx")

    # Tạo một đối tượng io.BytesIO để ghi dữ liệu vào
    output = io.BytesIO()

    # Ghi dữ liệu DataFrame vào đối tượng io.BytesIO
    data.to_excel(output, index=False)

    # Tạo nút tải với dữ liệu đã ghi vào đối tượng io.BytesIO
    btn = st.download_button(
        label="Download Excel File",
        data=output.getvalue(),  # Lấy dữ liệu từ đối tượng io.BytesIO
        file_name="ketqua.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # MIME type của file Excel
    )
#st.write(num_d)