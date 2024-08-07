import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
st.set_page_config(
    page_title="Trang Chủ",
    page_icon=":bar_chart:",
    #initial_sidebar_state = "expanded"
    layout= "wide",
    initial_sidebar_state = "collapsed",
)
# Đọc dữ liệu từ file Excel
df = pd.read_excel("./Book1.xlsx")
sf = pd.read_excel("./result.xlsx")
excel_file = "result.xlsx"
excel_file1 = "Book1.xlsx"
# Khai báo giá trị k để so sánh
def write_to_excel(ks, row, d, excel_file):
    row1 = row + 1
    ab = st.session_state.get("ex", None)
    gf = pd.DataFrame([ab])
    with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists='overlay') as writer:
        gf.to_excel(writer, startrow=row1, startcol=d, index=False, header=False)
    return
st.header("Thành tâm khấn nguyện 👏👏👏" )
while True:
    today = datetime.now()
    time = str(today - df.iloc[0, 0])
    time1 = int(str(time[:2]))
    if time1 != 1:
        st.progress(time1, text="Đang cập nhật dữ liệu")
        maeday = str(df.iloc[0, 0])
        date_object1 = datetime.strptime(maeday, '%Y-%m-%d %H:%M:%S')
        date_object2 = date_object1 + timedelta(days=1)
        maeday2 = str(date_object2)
        maeday1 = maeday2[:10]
        date_object = datetime.strptime(maeday1, '%Y-%m-%d')
        new_date_string = date_object.strftime('%d-%m-%Y')
        url = 'https://ketqua01.net/xo-so-mien-bac.php?ngay='+new_date_string
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        elements_with_id = soup.find(id='rs_0_0')
        div_text = elements_with_id.text
        new_row = {}
        new_row_df = pd.DataFrame([new_row])
        kf = pd.concat([df.iloc[:0], new_row_df, df.iloc[0:]], ignore_index=True)
        kf.to_excel(excel_file1, index=False)
        ks = date_object
        st.session_state["ex"] = ks
        write_to_excel(ks, 0, 0, excel_file1)
        ks1 = int(div_text)
        st.session_state["ex"] = ks1
        write_to_excel(ks1, 0, 1, excel_file1)
        time1 = time1-1
        df = pd.read_excel("./Book1.xlsx")
        st.rerun()
    if time1 == 1:
        df = pd.read_excel("./Book1.xlsx")
        st.subheader(df.iloc[0, 0])
        break
tab1, tab2, tab3 = st.tabs(["TÍNH TOÁN KẾT QUẢ", "TỔNG HỢP KẾT QUẢ", "KẾT QUẢ 2 CẦU"])
with tab2:
    st.subheader(df.iloc[0, 0])
    st.subheader(df.iloc[0, 1])
    nd = int(st.number_input("Độ dài của cầu",step = 1))
    kd = int(st.number_input("Ngày trong tháng:", step = 1))
    st.subheader(df.iloc[kd, 0])
    st.subheader(df.iloc[kd, 1])
    bd = 1
    #if bd == 0 :
        #bd = 5
        #st.write("Bên độ soi cầu là: ",bd)
    num_r = []
    numx = []
    numy = []
    num_d = []
    if nd > 2:
        for u in range(0, nd):
            x_u = str(int(df.iloc[u+kd, 1]))[-2:]
            y_u = df.iloc[u, 0]
            numx.append(x_u)
            numy.append(y_u)
            if u > 0:
                st.write(int(numx[u]) - int(numx[u-1]))
    st.write(str(numx))
    if nd == 3:
        for bd in range(13,16):
            st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
            if nd > 2:
                kml = kd + 1
                #st.write(df.iloc[kd-1, 0],df.iloc[kd-1, 1])
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
            if tl != 0:
                st.write("Số cầu thõa mãn là :",tl)
                st.write("Tỉ lệ ra số Lớn là :",round((lon/tl)*100,2),"%")
                st.write("Tỉ lệ ra số Bé là :",round((be/tl)*100,2),"%")
            else:
                st.write("Dữ liệu không có cầu này! Vui lòng chọn ngày cầu nhỏ hơn")
            num_r = []
        st.write(num_d)
    else:
        for bd in range(1,16):
            st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
            if nd > 2:
                kml = kd + 1
                #st.write(df.iloc[kd-1, 0],df.iloc[kd-1, 1])
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
            if tl != 0:
                st.write("Số cầu thõa mãn là :",tl)
                st.write("Tỉ lệ ra số Lớn là :",round((lon/tl)*100,2),"%")
                st.write("Tỉ lệ ra số Bé là :",round((be/tl)*100,2),"%")
            else:
                st.write("Dữ liệu không có cầu này! Vui lòng chọn ngày cầu nhỏ hơn")
            num_r = []
        st.write(num_d)
with tab3:
    st.subheader(df.iloc[0, 0])
    st.subheader(df.iloc[0, 1])
    nd1 = int(st.number_input("Số ngày soi",step = 1))
    jd = int(st.number_input("Số ngày bạn muốn tính + 1:",step = 1))
    bd = 1
    num_r = []
    numx = []
    numy = []
    num_d = []
    # Duyệt qua các hàng của DataFrame
    # st.write("Ngày dừng lại để tính toán",df.iloc[kd, 0])
    if st.button("Nhấn nút này để tính toán"):
        my_bar = st.progress(0)
        win = {}
        lose = {}
        hoa = {}
        for bd in range(1,16):
            win[bd] = []
            lose[bd] = []
            hoa[bd] = []
        for kd in range(1, jd):
            my_bar.progress(((kd) / (jd - 1)), "Đang tính toán, vui lòng đợi:")
            if nd1 > 2:
                for u in range(0, nd1):
                    x_u = str(int(df.iloc[u + kd, 1]))[-2:]
                    y_u = df.iloc[u, 0]
                    numx.append(x_u)
                    numy.append(y_u)
                    # if u > 0:
                    # st.write(int(numx[u]) - int(numx[u-1]))
            # st.write(str(numx),df.iloc[0, 0])
            # st.write(kd)
            for bd in range(1, 16):
                # st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
                # st.write(kd)
                if nd1 > 2:
                    kml = kd + 1
                    for i in range(kml, len(df) - 20):
                        l = int(
                            str(int(df.iloc[i, 1]))[-2:])  # Lấy hai ký tự cuối cùng của giá trị và chuyển thành chuỗi
                        l1 = int(str(int(df.iloc[i + 1, 1]))[-2:])
                        x1 = l1 - l
                        if (int(numx[1]) - int(numx[0])) - bd <= x1 <= (int(numx[1]) - int(numx[0])) + bd:
                            match_found = True
                            for p in range(2, nd1):
                                l_p = int(str(int(df.iloc[i + p, 1]))[-2:])
                                l_f = int(str(int(df.iloc[i + p - 1, 1]))[-2:])
                                x_p = l_p - l_f
                                if (int(numx[p]) - int(numx[p - 1])) - bd <= x_p <= (
                                        int(numx[p]) - int(numx[p - 1])) + bd:
                                    if p == nd1 - 1:
                                        lits = []
                                        for m in range(0, nd1):
                                            pl = i + m
                                            lits.append(df.iloc[pl, 1])
                                        num_r.append(str(int(df.iloc[i - 1, 1]))[-2:])
                                else:
                                    break
                    tl = len(num_r)
                    lon = 0
                    be = 0
                    for nu in range(0, tl):
                        kh = int(num_r[nu])
                        if kh > 50:
                            lon = lon + 1
                        else:
                            be = be + 1
                    if tl != 0:
                        gttt = int(str(int(df.iloc[kd - 1, 1]))[-2:])
                        if round((lon / tl) * 100, 2) > round((be / tl) * 100, 2):
                            if round((lon / tl) * 100, 2) > 50 and gttt >= 50:
                                win[bd].append(1)
                            if round((lon / tl) * 100, 2) > 50 and gttt < 50:
                                lose[bd].append(1)
                        else:
                            if round((be / tl) * 100, 2) > 50 and gttt < 50:
                                win[bd].append(1)
                            if round((be / tl) * 100, 2) > 50 and gttt >= 50:
                                lose[bd].append(1)
                        if round((lon / tl) * 100, 2) == round((be / tl) * 100, 2):
                            hoa[bd].append(1)
                    num_r = []
            numx = []
            numy = []
        for bd in range(1,16):
            exec(f'thang{bd} = {len(win[bd])}')
            exec(f'thua{bd} = {len(lose[bd])}')
            exec(f'bang{bd} = {len(hoa[bd])}')
        df = pd.DataFrame(
            [
                {"Kết quả" : "Thắng","1": thang1, "2": thang2, "3": thang3,"4": thang4,"5": thang5,"6": thang6,"7": thang7, "8": thang8,"9": thang9,"10": thang10,"11": thang11,"12": thang12,"13": thang13,"14": thang14,"15": thang15,},
                {"Kết quả" : "Thua","1": thua1, "2": thua2, "3": thua3, "4": thua4, "5": thua5, "6": thua6, "7": thua7, "8": thua8,
                 "9": thua9, "10": thua10, "11": thua11, "12": thua12, "13": thua13, "14": thua14, "15": thua15, },
                {"Kết quả" : "Hòa","1": bang1, "2": bang2, "3": bang3,"4": bang4,"5": bang5,"6": bang6,"7": bang7, "8": bang8,"9": bang9,"10": bang10,"11": bang11,"12": bang12,"13": bang13,"14": bang14,"15": bang15,},
            ]
        )
        st.dataframe(df, use_container_width=False)
with tab1:
    st.subheader(df.iloc[0, 0])
    st.subheader(df.iloc[0, 1])
    #nd = int(st.number_input("Độ dài của cầu",step = 1))
    kd = int(st.number_input("Chọn ngày trong tháng:", step = 1))
    st.subheader(df.iloc[kd, 0])
    st.subheader(df.iloc[kd, 1])
    bd = 1
    #if bd == 0 :
        #bd = 5
        #st.write("Bên độ soi cầu là: ",bd)
    col1, col2, col3 = st.columns([0.3, 0.3, 0.4], gap="small")
    with col1:
        st.header(f":red[Cầu 3]")
        nd = 3
        num_r = []
        numx = []
        numy = []
        num_d = []
        if nd > 2:
            for u in range(0, nd):
                x_u = str(int(df.iloc[u+kd, 1]))[-2:]
                y_u = df.iloc[u, 0]
                numx.append(x_u)
                numy.append(y_u)
                if u > 0:
                    st.write(int(numx[u]) - int(numx[u-1]))
        st.write(str(numx))
        for bd in range(1,10):
            #st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
            if nd > 2:
                kml = kd + 1
                #st.write(df.iloc[kd-1, 0],df.iloc[kd-1, 1])
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
            if tl >=10:
                st.subheader(f":blue[Số cầu thỏa mãn là:] {tl}")
                st.write("Tỉ lệ ra số Lớn là :",round((lon/tl)*100,2),"%")
                st.write("Tỉ lệ ra số Bé là :",round((be/tl)*100,2),"%")
                st.write("Hiệu số :",round((lon/tl)*100-(be/tl)*100,2),"%")
            #else:
                #st.write("Dữ liệu không có cầu này! Vui lòng chọn ngày cầu nhỏ hơn")
            num_r = []
        st.write(num_d)
    with col2:
        st.header(f":red[Cầu 4]")
        nd = 4
        num_h = []
        numx = []
        numy = []
        num_d = []
        if nd > 2:
            for u in range(0, nd):
                x_u = str(int(df.iloc[u+kd, 1]))[-2:]
                y_u = df.iloc[u, 0]
                numx.append(x_u)
                numy.append(y_u)
                if u > 0:
                    st.write(int(numx[u]) - int(numx[u-1]))
        st.write(str(numx))
        for bd in range(5,16):
            #st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
            if nd > 2:
                kml = kd + 1
                #st.write(df.iloc[kd-1, 0],df.iloc[kd-1, 1])
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
                                    num_h.append(str(int(df.iloc[i-1, 1]))[-2:])
                                    #st.write(df.iloc[i, 0])
                                    #st.write(lits,)
                                    #st.write(str(int(df.iloc[i-1, 1]))[-2:])
                            else:
                                break
                #st.write("Các chỉ số hàng thỏa mãn điều kiện:")
                #st.write(str(num_r))
            tl = len(num_h)
            #st.write(tl)
            #st.write(nd)
            lon = 0
            be = 0
            for nu in range(0,tl):
                kh = int(num_h[nu])
                if kh > 50:
                    lon = lon + 1
                else:
                    be = be + 1
            if tl >= 10:
                st.subheader(f":red[Số cầu thỏa mãn là:] {tl}")
                st.write("Tỉ lệ ra số Lớn là :",round((lon/tl)*100,2),"%")
                st.write("Tỉ lệ ra số Bé là :",round((be/tl)*100,2),"%")
                st.write("Hiệu số :",round((lon/tl)*100-(be/tl)*100,2),"%")
            #else:
                #st.write("Dữ liệu không có cầu này! Vui lòng chọn ngày cầu nhỏ hơn")
            num_h = []
        st.write(num_d)
    with col3:
        st.header(f":red[Cầu 5]")
        nd = 5
        num_o = []
        numx = []
        numy = []
        num_d = []
        if nd > 2:
            for u in range(0, nd):
                x_u = str(int(df.iloc[u+kd, 1]))[-2:]
                y_u = df.iloc[u, 0]
                numx.append(x_u)
                numy.append(y_u)
                if u > 0:
                    st.write(int(numx[u]) - int(numx[u-1]))
        st.write(str(numx))
        for bd in range(10,20):
            #st.subheader(f":red[Biên độ dao động của cầu = {bd}]")
            if nd > 2:
                kml = kd + 1
                #st.write(df.iloc[kd-1, 0],df.iloc[kd-1, 1])
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
                                    num_o.append(str(int(df.iloc[i-1, 1]))[-2:])
                                    #st.write(df.iloc[i, 0])
                                    #st.write(lits,)
                                    #st.write(str(int(df.iloc[i-1, 1]))[-2:])
                            else:
                                break
                #st.write("Các chỉ số hàng thỏa mãn điều kiện:")
                #st.write(str(num_r))
            tl = len(num_o)
            #st.write(tl)
            #st.write(nd)
            lon = 0
            be = 0
            for nu in range(0,tl):
                kh = int(num_o[nu])
                if kh > 50:
                    lon = lon + 1
                else:
                    be = be + 1
            if tl >=10:
                st.subheader(f":blue[Số cầu thỏa mãn là:] {tl}")
                st.write("Tỉ lệ ra số Lớn là :",round((lon/tl)*100,2),"%")
                st.write("Tỉ lệ ra số Bé là :",round((be/tl)*100,2),"%")
                st.write("Hiệu số :",round((lon/tl)*100-(be/tl)*100,2),"%")
            #else:
                #st.write("Dữ liệu không có cầu này! Vui lòng chọn ngày cầu nhỏ hơn")
            num_o = []
        st.write(num_d)
        
