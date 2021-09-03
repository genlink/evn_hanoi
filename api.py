"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import datetime
import logging
import requests, json, time
from bs4 import BeautifulSoup
from datetime import timedelta
import locale

locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

class EVNHN:

    INTERVAL_6MIN = "6min"
    INTERVAL_DAY = "day"


    def _get_details(self,makhachhang):
        self.makhachhang = makhachhang
        self.mainURL = 'http://42.112.213.225:8050/Service.asmx/'
        ma_khachhang = self.makhachhang
        url_ma_ddo = self.mainURL + 'CHECK_DDO?ma_kh=' + ma_khachhang
        ma_ddo = requests.get(url_ma_ddo)
        ma_ddo = ma_ddo.text
        ma_ddo = ma_ddo.split('<MA_DDO>')
        ma_ddo = ma_ddo[1][:ma_ddo[1].find('</MA_DDO')]
        today_date = datetime.datetime.now()
        past_day = today_date - datetime.timedelta(days=3)
        url_sanluong_day = self.mainURL+'GET_THONGSO_VANHANH_SANLUONG_THEONGAY?ma_ddo='+ma_ddo+'&tu_ngay='+past_day.strftime("%d/%m/%Y")+'&den_ngay='+today_date.strftime("%d/%m/%Y")
        sanluong_day = requests.get(url_sanluong_day)
        sanluong_day = BeautifulSoup(sanluong_day.text, 'xml')
        sanluong_day = sanluong_day.find_all("CHI_SO")
        dem = len(sanluong_day)
        if dem == 3:
            sanluong_day.append(sanluong_day[2])
        sanluong_day1 = round(float(sanluong_day[3].text) - float(sanluong_day[2].text),2)
        sanluong_day2 = round(float(sanluong_day[2].text) - float(sanluong_day[1].text),2)
        sanluong_day3 = round(float(sanluong_day[1].text) - float(sanluong_day[0].text),2)
        '''Lay thong tin hoa don 3 thang gan nhat'''
        nam_hientai = today_date.year
        thang = [today_date.strftime("%m")]
        for _ in range(0, 2):
            today_date = today_date.replace(day=1) - datetime.timedelta(days=1)
            thang.append(today_date.strftime("%m"))
        tien_dien =[]
        thanh_toan = []
        san_luong = []
        for num in range(int(thang[2]),int(thang[0])+1):
            print(num)
            url_tt_hoadon = self.mainURL+'get_hdon_ttoan?ma_kh='+ma_khachhang+'&ky=1&thang='+str(num)+'&nam='+str(nam_hientai)
            tt_hoadon = requests.get(url_tt_hoadon)
            tt_hoadon = BeautifulSoup(tt_hoadon.text, 'xml')
            check = tt_hoadon.find('NewDataSet')
            if not check :
                tt_tiendien = 'Chưa cập nhật'
                tt_san_luong = 'Chưa cập nhật'
                kt_thanh_toan = 'Chưa cập nhật'
            else :
                tt_tiendien = tt_hoadon.find('TONG_TIEN')
                tt_tiendien = tt_tiendien.text
                kt_thanh_toan = tt_hoadon.find('TIEN_NO')
                kt_thanh_toan = kt_thanh_toan.text
                tt_san_luong = tt_hoadon.find('DIEN_TTHU')
                tt_san_luong = tt_san_luong.text
            tien_dien.append(tt_tiendien)
            thanh_toan.append(kt_thanh_toan)
            san_luong.append(tt_san_luong)
        thang.reverse()
        for i in range(len(thanh_toan)):
            if thanh_toan[i] == '0' :
                thanh_toan[i] = 'Đã thanh toán'
            else:
                thanh_toan[i] = 'Chưa thanh toán'+thanh_toan[i]

#        tien_thangtruocnua = locale.currency(float(tien_dien[0]), grouping=True)
#        tien_thangtruoc = locale.currency(float(tien_dien[1]), grouping=True)
#        tien_thangnay = locale.currency(float(tien_dien[2]), grouping=True)
        json_data = {
            'state': sanluong_day1,
            'ma_ddo': ma_ddo,
            'sanluong_day1': sanluong_day1,
            'sanluong_day2': sanluong_day2,
            'sanluong_day3': sanluong_day3,
            'thang_truoc_nua': thang[0],
            'thang_truoc': thang[1],
            'thang_nay': thang[2],
            'sanluong_thangtruocnua': san_luong[0],
            'sanluong_thangtruoc': san_luong[1],
            'sanluong_thangnay': san_luong[2],
            'tiendien_thangtruocnua': tien_dien[0],
            'tiendien_thangtruoc': tien_dien[1],
            'tiendien_thangnay': tien_dien[2],
            'thanhtoan_thangtruocnua': thanh_toan[0],
            'thanhtoan_thangtruoc': thanh_toan[1],
            'thanhtoan_thangnay': thanh_toan[2]
        }
        return json_data

    def get_evn_hanoi(self,makhachhang):
        return self._get_details(makhachhang)


